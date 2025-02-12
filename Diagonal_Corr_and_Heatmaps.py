import numpy

import matplotlib.pyplot as plt

import seaborn as sns

import os

from Global import (beats, map_date, correlation_min)


# find_diagonal_corr function identifies the highest correlated 8 diagonal beats between two song and
# further identifies the starting and ending beats in both songs for the highest correlated diagonal
def find_diagonal_corr(d_matrix, min_beats):
    # correlation matrix from Comparison Class object is passed in as a parameter
    num_beats = min_beats # d_matrix.shape[0]
    beats_window = 8  # optional to replace "beats" in order to get more audio time
    max_corr = -numpy.inf
    best_offset = 0
    y_start = 0
    y_end = 0
    x_start = 0
    x_end = 0

    # Loop over all possible diagonals (offsets)
    for offset in range(-num_beats + beats_window, num_beats - beats_window + 1):
        diagonal = numpy.diag(d_matrix, k=offset)
        # Get the diagonal elements for this offset
        for start in range(len(diagonal) - beats_window + 1):
            # Loop through all possible 8-beat windows in this diagonal
            current_window = diagonal[start:start + beats_window]
            corr = numpy.mean(current_window)
            # mean of the correlations in this window

            if corr > max_corr:
                max_corr = corr
                best_offset = offset
                # //ignore: 10/29 y_start = start
                # //ignore: 10/29 y_end = y_start + beats_window
                if best_offset < 0: # added 10/29
                    y_start = start + abs(best_offset)
                    y_end = y_start + beats_window
                    x_start = start
                    x_end = x_start + beats_window
                # //ignore:10/29 else:
                    # //ignore:10/29 x_start = y_start
                    # //ignore:10/29 x_end = y_end
                # Calculate x-axis indices based on the offset
                if best_offset >= 0: # added 10/29
                    x_start = start + best_offset
                    x_end = x_start + beats_window
                    y_start = start
                    y_end = y_start + beats_window
                # 10/29 else:
                    # 10/29 x_start = y_start
                    #10/29 x_end = y_end
    # print(f"Best correlation sum: {max_corr}")
    # print(f"Best diagonal offset: {best_offset}")
    # print(f"Starting beat of the best window: {y_start}")
    return max_corr, best_offset, y_start, y_end, x_start, x_end


def dispute_heatmap_labels(i_d):
    if i_d == 0:
        return 'Satriani_(Y) vs. Coldplay_(X)', 'Satriani', 'Coldplay'
    if i_d == 1:
        return 'TomPetty_(Y) vs. SamSmith_(X)', 'Tom Petty', 'Sam Smith'
    if i_d == 2:
        return 'TheChiffons_(Y) vs. GHarrison_(X)', 'Chiffons', 'Harrison'
    if i_d == 3:
        return 'RollingStones_(Y) vs. TheVerve_(X)', 'Stones', 'The Verve'
    if i_d == 4:
        return 'MGaye_(Y) vs. Sheeran_(X)', 'M. Gaye', 'E. Sheeran'
    if i_d == 5:
        return 'HueyLewis_(Y) vs. RayParker_(X)', 'H. Lewis', 'Ray Parker'
    if i_d == 6:
        return 'BeachBoys_(Y) vs. ChuckBerry_(X)', 'Beach Boys', 'C. Berry'
    if i_d == 7:
        return 'Oasis_(Y) vs. T-Rex_(X)', 'Oasis', 'T-Rex'


def dispute_diagonal_heatmap(d_matrix, d_id, d_corr, d_y_start, d_x_start, d_offset):
    temp_new_start_beat = 0
    temp_new_end_beat = 0
    d = 0
    min_val = 0
    max_val = 1
    # 10/29 band = min(abs(d_corr - (-1)), abs(1 - d_corr))
    # 10/29 min_val = d_corr - band
    # 10/29 max_val = d_corr + band

    plt.figure(figsize=(6, 4))
    d_axis_length = d_matrix.shape[0]
    d_map = sns.heatmap(d_matrix, annot=False, cmap='coolwarm', xticklabels=numpy.arange(d_axis_length),
                        yticklabels=numpy.arange(d_axis_length), vmin=min_val, vmax=max_val)
    d_map.invert_yaxis()

    for dd in range(8):  # added 10/29
        d_col = d_y_start + dd
        d_row = d_x_start + dd
        d_map.add_patch(plt.Rectangle((d_row, d_col), 1, 1, fill=False, edgecolor='black',
                                      lw=1))  # added 10/29
    # 10/29  if d_offset > 0:
        # 10/29 for d in range(8):
            # 10/29 d_row = d_y_start + d
            # 10/29 d_col = d_y_start + d + d_offset
            # 10/29 temp_new_start_beat = d_y_start + abs(d_offset)   # new start beat on x axis
            # 10/29 temp_new_end_beat = temp_new_start_beat + 8            # new end beat on x axis
            # 10/29 change_x_beats = True
            # 10/29 d_map.add_patch(plt.Rectangle((d_col, d_row), 1, 1, fill=False, edgecolor='black',
                    # 10/29  lw=1))

    # 10/29 if d_offset < 0:
        # 10/29 for d in range(8):
        # 10/29  d_col = d_y_start + d
            # 10/29 d_row = d_y_start + d + abs(d_offset)
            # 10/29 temp_new_start_beat = d_y_start + abs(d_offset)  # new start beat on y axis
            # 10/29 temp_new_end_beat = temp_new_start_beat + 8           # new end beat on y axis
            # 10/29 d_map.add_patch(plt.Rectangle((d_col, d_row), 1, 1, fill=False, edgecolor='black',
                    # 10/29  lw=1))
    dispute_title, dy_label, dx_label = dispute_heatmap_labels(d_id)
    d_map.tick_params(axis='y', labelsize=3)
    d_map.tick_params(axis='x', labelsize=3)

    d_file_title = str(d_corr) + dispute_title + str(d_offset) + '_' + map_date + '.svg'
    plt.title(str(d_corr) + dispute_title + str(d_offset))
    plt.xlabel(dx_label)
    plt.ylabel(dy_label)
    plt.savefig(f'pickles/NEW_IMP/DISPUTE/heatmaps/{d_file_title}', format='svg')
    plt.close()

    return


def validate_heatmap_labels(v_d):
    if v_d == 0:
        return 'Uptown_Funk(Y) vs. Uptown_Funk(X)', 'Upt. Funk', 'Upt. Funk'
    if v_d == 1:
        return 'Uptown_Funk(Y) vs. 18 secs delay (X)', 'Upt. Funk', 'Delayed'


def validate_diagonal_heatmap(v_matrix, v_id, v_corr, v_offset, v_start, v_end, v_axis_length):
    plt.figure(figsize=(6, 4))
    v_map = sns.heatmap(v_matrix, annot=False, cmap='coolwarm', xticklabels=numpy.arange(v_axis_length),
                        yticklabels=numpy.arange(v_axis_length), vmin=0, vmax=1)
    v_map.invert_yaxis()

    for v in range(beats):
        v_row = v_start + v
        v_col = v_start + v + v_offset
        v_map.add_patch(plt.Rectangle((v_col, v_row), 1, 1, fill=False, edgecolor='black', lw=1))

    validate_title, vy_label, vx_label = validate_heatmap_labels(v_id)
    v_file_title = str(v_corr) + '_' + validate_title + '_valid_' + str(v_offset) + '_' + map_date + '.svg'
    v_end = v_end - 1

    plt.title(str(v_corr) + '_beats_' + str(v_start) + '-' + str(v_end))
    plt.xlabel(vx_label)
    plt.ylabel(vy_label)
    v_map.tick_params(axis='y', labelsize=3)
    v_map.tick_params(axis='x', labelsize=3)
    plt.savefig(f'pickles/NEW_IMP/VALIDATE/heatmaps/{v_file_title}', format='svg')
    plt.close()

    return v_map


def suno_diagonal_heatmap(suno_diag_matrix, suno_diag_comp, diag_id):   # comp_num, cid)
    plt.figure(figsize=(6, 4))
    sdc = suno_diag_comp
    p1 = sdc.y_promptID + 1
    p2 = sdc.x_promptID + 1
    sd_base_dir = f'pickles/NEW_IMP/SUNO/heatmaps/{map_date}/{p1}P_v_{p2}P'
    os.makedirs(sd_base_dir, exist_ok=True)
    # 10/29 suno_d_start = sdc.y_start
    # 10/29 suno_d_offset = sdc.offset
    suno_y_start = sdc.y_start  # added 10/29
    suno_x_start = sdc.x_start  # added 10/29
    suno_d_axis_length = sdc.length
    suno_diagonal_map = sns.heatmap(suno_diag_matrix, annot=False, cmap='coolwarm',
                                    xticklabels=numpy.arange(suno_d_axis_length),
                                    yticklabels=numpy.arange(suno_d_axis_length), vmin=0, vmax=1)
    sdmap = suno_diagonal_map
    sdmap.invert_yaxis()

    # 10/29 if suno_d_offset > 0:
        # 10/29 for sd in range(8):
            # 10/29 suno_d_row = suno_d_start + sd
            # 10/29 suno_d_col = suno_d_start + sd + suno_d_offset
            # suno_temp_new_start_beat = d_y_start + abs(d_offset)   # new start beat on x axis
            # suno_temp_new_end_beat = temp_new_start_beat + 8            # new end beat on x axis
            # change_x_beats = True
            # 10/29 sdmap.add_patch(plt.Rectangle((suno_d_col, suno_d_row), 1, 1, fill=False, edgecolor='black',
                                               # lw=1))

    # 10/29 if suno_d_offset < 0:
        # 10/29 for sd in range(8):
            # 10/29 suno_d_col = suno_d_start + sd
            # 10/29 suno_d_row = suno_d_start + sd + abs(suno_d_offset)

            # suno_temp_new_start_beat = d_y_start + abs(d_offset)   # new start beat on y axis
            # suno_temp_new_end_beat = temp_new_start_beat + 8            # new end beat on y axis
            # change_x_beats = True
            # 10/29 sdmap.add_patch(plt.Rectangle((suno_d_col, suno_d_row), 1, 1, fill=False, edgecolor='black',
                                               # lw=1))
    for sd in range(8): # added 10/29
        suno_col = suno_y_start + sd
        suno_row = suno_x_start + sd
        sdmap.add_patch(plt.Rectangle((suno_row, suno_col), 1, 1, fill=False, edgecolor='black',
                                  lw=1)) # added 10/29

    suno_d_y_prompt = sdc.y_promptID + 1
    suno_d_y_student = sdc.y_studentID + 1
    suno_d_y_song = sdc.y_songID + 1
    suno_d_y_label = 'P' + str(suno_d_y_prompt) + ' ' + 'St' + str(suno_d_y_student) + ' ' + 'sg' + str(suno_d_y_song)
    plt.ylabel(suno_d_y_label)
    sdmap.tick_params(axis='y', labelsize=2)

    suno_d_x_prompt = sdc.x_promptID + 1
    suno_d_x_student = sdc.x_studentID + 1
    suno_d_x_song = sdc.x_songID + 1
    suno_d_x_label = 'P' + str(suno_d_x_prompt) + ' ' + 'St' + str(suno_d_x_student) + ' ' + 'sg' + str(suno_d_x_song)
    plt.xlabel(suno_d_x_label)
    sdmap.tick_params(axis='x', labelsize=2)

    suno_d_title = str(sdc.d_corr) + '_' + suno_d_y_label + ' _v_ ' + suno_d_x_label + '_' + str(sdc.y_start)
    suno_d_file_title = str(sdc.d_corr) + f'__{diag_id}_' +  '_map_' + map_date + '.svg'

    if sdc.offset < 0:
        plt.title('offset_' + str(sdc.offset) + '_' + 'start_Y_' + str(sdc.y_start) + '_end_Y_' + str(sdc.y_end))
    else:
        plt.title('offset_' + str(sdc.offset) + '_' + 'start_X_' + str(sdc.x_start) + '_end_X_' + str(sdc.x_end))
    # plt.savefig(f'heatmaps/suno/diagonal/{suno_d_file_title}', format='svg')
    # plt.savefig(f'pickles/NEW_IMP/SUNO/heatmaps/{comp_num}/{cid}/{suno_d_file_title}', format='svg')
    plt.savefig(os.path.join(sd_base_dir, suno_d_file_title), format='svg')
    plt.close()

    return sdmap


def negative_offset_heatmap(n_matrix, n_comp):
    if n_comp.diag_corr < correlation_min:
        return
    else:
        n_axis_length = n_comp.length
        n_offset = n_comp.offset

        y_coords = numpy.arange(n_comp.y_start, n_comp.y_end)
        x_coords = y_coords + abs(n_offset)
        y_coords_inverted = n_axis_length - y_coords

        plt.figure(figsize=(6, 4))
        n_map = sns.heatmap(n_matrix, annot=False, cmap='coolwarm', xticklabels=numpy.arange(n_axis_length),
                                      yticklabels=numpy.arange(n_axis_length), vmin=0, vmax=1)
        for x, y in zip(x_coords, y_coords_inverted):
            if 0 <= x < n_axis_length and 0 <= y < n_axis_length:  # Ensure coordinates are within bounds
                n_map.add_patch(plt.Rectangle((x, y), 1, 1, fill=False, edgecolor='black', lw=1))

        n_map.invert_yaxis()


        yn_prompt = n_comp.y_promptID + 1
        yn_student = n_comp.y_studentID + 1
        yn_song = n_comp.y_songID + 1
        xn_prompt = n_comp.x_promptID + 1
        xn_student = n_comp.x_studentID + 1
        xn_song = n_comp.x_songID + 1

        yn_label = 'P' + str(yn_prompt) + ' ' + 'St' + str(yn_student) + ' ' + 'sg' + str(yn_song)
        xn_label = 'P' + str(xn_prompt) + ' ' + 'St' + str(xn_student) + ' ' + 'sg' + str(xn_song)
        n_title = str(n_comp.diag_corr) + '_' + yn_label + ' v ' + xn_label
        plt.xlabel(xn_label)
        plt.ylabel(yn_label)
        plt.title(n_title)
        n_file_title = n_title + '_' + map_date + '_' + str(n_comp.offset) + '.svg'
        plt.savefig(f'heatmaps/suno/{n_file_title}', format='svg')
        plt.close()

        return n_map




