from Global import beats, map_date

import numpy

import seaborn as sns

import matplotlib.pyplot as plt


def find_straight_corr(current_matrix, beats_length):
    max_horizontal_mean, max_vertical_mean,  max_mean = 0, 0, 0
    beat_index1, beat_index2 = 0, 0
    h_beat_index1, h_beat_index2 = 0, 0
    v_beat_index1, v_beat_index2 = 0, 0
    straight_constant = 0
    constant_h_axis_val = 0
    constant_v_axis_val = 0
    segment_corr_list = []
    is_horizontal = True

    # Finding horizontal mean correlations
    for y1 in range(beats_length):
        for x1 in range(beats_length - beats + 1):
            # print(f' length of this horiz segment: {current_matrix[y1, h1:h1 + beats].shape}')
            horizontal_mean = numpy.mean(current_matrix[y1, x1:x1 + beats])
            # print(f' mean of this horiz segment: {horizontal_mean}')
            # print('')
            segment_corr_list.append(horizontal_mean)
            if horizontal_mean > max_horizontal_mean:
                max_horizontal_mean = horizontal_mean
                h_beat_index1 = x1
                h_beat_index2 = x1 + beats
                constant_v_axis_val = y1
    # min_h_mean = min(segment_corr_list)
    segment_corr_list = []
    # print('done with horiz correlations')
    # Finding vertical mean correlations
    for y2 in range(beats_length):
        for x2 in range(beats_length - beats + 1):
            # print(f' length of this vert segment: {current_matrix[y2:y2 + beats, x2].shape}')
            vertical_mean = numpy.mean(current_matrix[y2:y2 + beats, x2])
            # print(f' mean of this vert segment: {vertical_mean}')
            # print('')
            segment_corr_list.append(vertical_mean)
            if vertical_mean > max_vertical_mean:
                max_vertical_mean = vertical_mean
                v_beat_index1 = y2
                v_beat_index2 = y2 + beats
                constant_h_axis_val = x2
    # min_v_mean = min(segment_corr_list)
    if max_horizontal_mean > max_vertical_mean:
        max_mean = max_horizontal_mean
        beat_index1 = h_beat_index1
        beat_index2 = h_beat_index2
        straight_constant = constant_v_axis_val
    if max_vertical_mean > max_horizontal_mean:
        max_mean = max_vertical_mean
        beat_index1 = v_beat_index1
        beat_index2 = v_beat_index2
        straight_constant = constant_h_axis_val
        is_horizontal = False

    # return min(min_h_mean, min_v_mean), max_mean, beat_index1, beat_index2, is_horizontal
    return max_mean, beat_index1, beat_index2, is_horizontal, straight_constant


def suno_straight_heatmap(suno_straight_matrix, suno_straight_comp):
    ssc = suno_straight_comp
    suno_s_axis_length = ssc.length
    constant_val = ssc.const

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    suno_straight_map = sns.heatmap(suno_straight_matrix, annot=False, cmap='coolwarm',
                                    xticklabels=numpy.arange(suno_s_axis_length),
                                    yticklabels=numpy.arange(suno_s_axis_length), vmin=0, vmax=1)
    ssmap = suno_straight_map

    if ssc.horizontal:
        # horizontal correlation along x-axis
        x_crds = numpy.arange(ssc.y_start, ssc.y_end)  # x-coordinates
        y_value = constant_val  # set the y-value 
        y_inverted = suno_s_axis_length - y_value  # transform for inverted y-axis
        for x in x_crds:  # x-coordinates vary 
            ssmap.add_patch(plt.Rectangle((y_inverted, x), 1, 1, fill=False, edgecolor='black', lw=1))
    else:
        # vertical correlation along y-axis
        y_crds = numpy.arange(ssc.y_start, ssc.y_end)  # y-coordinates
        y_crds_inverted = suno_s_axis_length - y_crds  # transform for inverted y-axis
        x_value = constant_val  # set the x-value 
        for y in y_crds_inverted:  # y-coordinates vary 
            ssmap.add_patch(plt.Rectangle((y, x_value), 1, 1, fill=False, edgecolor='black', lw=1))

    ssmap.invert_yaxis()

    suno_s_y_prompt = ssc.y_promptID + 1
    suno_s_y_student = ssc.y_studentID + 1
    suno_s_y_song = ssc.y_songID + 1
    suno_s_y_label = 'P' + str(suno_s_y_prompt) + ' ' + 'St' + str(suno_s_y_student) + ' ' + 'sg' + str(suno_s_y_song)
    plt.ylabel(suno_s_y_label)
    ssmap.tick_params(axis='y', labelsize=2)

    suno_s_x_prompt = ssc.x_promptID + 1
    suno_s_x_student = ssc.x_studentID + 1
    suno_s_x_song = ssc.x_songID + 1
    suno_s_x_label = 'P' + str(suno_s_x_prompt) + ' ' + 'St' + str(suno_s_x_student) + ' ' + 'sg' + str(suno_s_x_song)
    suno_s_x_label = suno_s_x_label
    plt.xlabel(suno_s_x_label)
    ssmap.tick_params(axis='x', labelsize=2)

    suno_s_title = str(ssc.s_corr) + '_' + suno_s_y_label + ' v ' + suno_s_x_label
    suno_s_file_title = suno_s_title + '_straight_' + map_date + '.svg'

    plt.title(str(ssc.s_corr) + 'start_' + str(ssc.y_start) + ' ' + '_end_' + str(ssc.y_end))
    plt.savefig(f'heatmaps/suno/straight/{suno_s_file_title}', format='svg')
    plt.close()

    return ssmap
