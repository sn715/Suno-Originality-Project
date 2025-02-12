from Song_Class import Song

# from Extract_Audio import extract_audio

from Diagonal_Corr_and_Heatmaps import suno_diagonal_heatmap

import pickle

import random

import numpy

import matplotlib.pyplot as plt

import seaborn as sns

from Global import (beats, map_date, correlation_min, to_load_pickle_date)

from Common_Functions import common_get_prompt_list, common_suno_diagonal_heatmap

from Diagonal_Corr_and_Heatmaps import find_diagonal_corr

from Straight_Corr_and_Heatmaps import find_straight_corr


class Comparison:
    def __init__(self, the_y_song, the_x_song, the_shared_length):
        self.y_promptID = the_y_song.prompt
        self.y_studentID = the_y_song.student
        self.y_songID = the_y_song.song
        self.x_promptID = the_x_song.prompt
        self.x_studentID = the_x_song.student
        self.x_songID = the_x_song.song
        self.length = the_shared_length
        self.matrix = numpy.zeros((the_shared_length, the_shared_length))


class Diagonal(Comparison):
    def __init__(self, the_y_song, the_x_song, the_shared_length, diag_correlation, diag_y_start_beat, diag_y_end_beat,
                 diag_x_start_beat, diag_x_end_beat, the_offset):
        super().__init__(the_y_song, the_x_song, the_shared_length)
        self.d_corr = round(diag_correlation, 4)
        self.y_start = diag_y_start_beat
        self.y_end = diag_y_end_beat
        self.x_start = diag_x_start_beat
        self.x_end = diag_x_end_beat
        self.offset = the_offset
        # dynamically added: self.x_extract =
        # dynamically added: self.y_extract =
        # dynamically added: self.comp_id =


class Straight(Comparison):
    def __init__(self, the_y_song, the_x_song, the_shared_length, straight_correlation, straight_start_beat,
                 straight_end_beat, is_horizontal, constant):
        super().__init__(the_y_song, the_x_song, the_shared_length)
        self.s_corr = round(straight_correlation, 4)
        self.start = straight_start_beat
        self.end = straight_end_beat
        self.horizontal = is_horizontal
        self.const = constant


def create_suno_diagonal_compare(d_y_song, d_x_song, d_shared_length, d_cmp_matrix):
    d_corr, d_offset, d_y_start, d_y_end, d_x_start, d_x_end = find_diagonal_corr(d_cmp_matrix, d_shared_length)
    # find_diagonal_corr function located in Diagonal_Corr_and_Heatmaps.py
    diagonal_comparison = Diagonal(d_y_song, d_x_song, d_shared_length, d_corr, d_y_start,
                                   d_y_end, d_x_start, d_x_end, d_offset)
    # create Diagonal Class Object defined above which inherits from Comparison Class object defined above
    diagonal_comparison.matrix = d_cmp_matrix
    return diagonal_comparison


def suno_straight_compare(s_y_song, s_x_song, s_shared_length, s_cmp_matrix):
    s_corr, s_start, s_end, is_this_horizontal, s_constant = find_straight_corr(s_cmp_matrix, s_shared_length)
    straight_comparison = Straight(s_y_song, s_x_song, s_shared_length, s_corr, s_start, s_end, is_this_horizontal,
                                   s_constant)
    return straight_comparison


def get_songs(this_list, cmpr, pre_fix):
    first1 = str(cmpr.y_promptID) + '_' + str(cmpr.y_studentID) + '_' + str(cmpr.y_songID)
    second1 = str(cmpr.x_promptID) + '_' + str(cmpr.x_studentID) + '_' + str(cmpr.x_songID)
    print(f'First Song: {first1} & Second Song: {second1}')
    print(f' **Diagonal Corr: {cmpr.d_corr}')
    print(f' *** Offset: {cmpr.offset}')
    print(f' ------ Y Beats {cmpr.y_start} to {cmpr.y_end}')
    print(f' ------ X Beats {cmpr.x_start} to {cmpr.x_end}')
    print(f' ------------------------------------------------')
    print(' ')
    m = 0
    complete = False
    while m < (len(this_list)) and not complete:
        y_student = this_list[m]
        for y_song in y_student:
            if y_song.student == cmpr.y_studentID and y_song.song == cmpr.y_songID and not complete:
                this_y_song = y_song
                print('^^^^^ found y song ^^^^^^')
                n = 0
                while n < (len(this_list)) and not complete:
                    x_student = this_list[n]
                    for x_song in x_student:
                        if x_song.student == cmpr.x_studentID and x_song.song == cmpr.x_songID and not complete:
                            this_x_song = x_song
                            print('^^^^^ found x song ^^^^^^')
                            if type(this_y_song) is Song and type(this_x_song) is Song:
                                print(' Song Objects found ')
                                # temp_matrix = numpy.zeros((cmpr.length, cmpr.length))
                                # for a in range(cmpr.length):
                                    # for b in range(cmpr.length):
                                        # temp_matrix[b, a] = numpy.corrcoef(this_y_song.mean_chroma[a],
                                                                           # this_x_song.mean_chroma[b])[0, 1]
                                cp_id = extract_audio(this_y_song, this_x_song, cmpr, pre_fix)
                                common_suno_diagonal_heatmap(cmpr.matrix, cmpr, pre_fix)
                                complete = True
                                break
                    n = n + 1
        m = m + 1
    print('done getting songs')
    print(' ')
    return






# for negative offsets (below)
def plot_heatmap_with_diagonal(correlation_matrix, cp):
    num_beats = correlation_matrix.shape[0]
    best_start = cp.y_start
    offset = cp.offset

    # Create the heatmap
    plt.figure(figsize=(12, 10))
    ax = sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', cbar=True, vmin=0, vmax=1)

    # Invert the y-axis for the heatmap
    ax.invert_yaxis()

    # Adjust diagonal coordinates for inverted y-axis

    for i in range(beats):
        x = best_start + i + abs(offset)  # X-coordinate (column index in the heatmap)
        y_original = best_start + offset + i  # Y-coordinate in non-inverted system (where offset is calculated)
        y_inverted = num_beats - y_original - 1
        ax.add_patch(plt.Rectangle((x, y_inverted), 1, 1, fill=False, edgecolor='black', lw=1))

    yn_prompt = cp.y_promptID + 1
    yn_student = cp.y_studentID + 1
    yn_song = cp.y_songID + 1
    xn_prompt = cp.x_promptID + 1
    xn_student = cp.x_studentID + 1
    xn_song = cp.x_songID + 1

    yn_label = 'P' + str(yn_prompt) + ' ' + 'St' + str(yn_student) + ' ' + 'sg' + str(yn_song)
    xn_label = 'P' + str(xn_prompt) + ' ' + 'St' + str(xn_student) + ' ' + 'sg' + str(xn_song)
    n_title = str(cp.diag_corr) + '_' + yn_label + ' v ' + xn_label
    plt.xlabel(xn_label)
    plt.ylabel(yn_label)
    plt.title(str(cp.diag_corr) + '_Start_' + str(cp.y_start) + '_End_' + str(cp.y_end))
    n_file_title = n_title + '_' + map_date + '_' + str(offset) + '.svg'
    plt.savefig(f'heatmaps/suno/{n_file_title}', format='svg')
    plt.close()

    return ax


