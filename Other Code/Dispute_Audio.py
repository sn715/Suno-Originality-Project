from Dispute_Song_Class import Dispute_Song

from Global import (dispute, num_of_disputes, dispute_songs_at, trim, chroma_analysis, to_save_pickle_date,
                    to_load_pickle_date, dispute_heatmaps, do_diagonal, do_straight)

from Diagonal_Corr_and_Heatmaps import find_diagonal_corr, dispute_diagonal_heatmap

from Straight_Corr_and_Heatmaps import find_straight_corr

from Extract_Audio import extract_dispute_audio

from Chroma_Utilities import chroma_of_frames, get_chroma, mean_beat_chroma, beat_group_corr

from pathlib import Path

import os

import pickle

import librosa.feature

import numpy


if dispute:
    dispute_list = [[] for _ in range(num_of_disputes)]
    print(' begin processing DISPUTE audio')
    dispute_root = Path.cwd() / dispute_songs_at
    dispute_num = 0
    for this_dispute in dispute_root.iterdir():
        dispute_list[dispute_num] = []
        current_dispute = dispute_list[dispute_num]
        song = 0
        for this_song in this_dispute.iterdir():
            print(f'dispute_num: {dispute_num}  song: {song} ')
            if os.path.isfile(this_song):
                audio, sr = librosa.load(this_song, sr=None, duration=trim)
                tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
                print(f'dispute: {dispute_num}  song: {song} ')
                dispute_song = Dispute_Song(dispute_num, song, song_audio=audio, song_sr=sr, beat_frames=beat_frames)
                if chroma_analysis:
                    get_chroma(song_for_chroma=dispute_song)
                    chroma_of_frames(song_for_frames=dispute_song)
                    mean_beat_chroma(rolling_beats_song=dispute_song)
                current_dispute.append(dispute_song)
                song = song + 1
        dispute_num = dispute_num + 1
    print('')
    with open(f'pickles/NEW_IMP/DISPUTE/{to_save_pickle_date}_all_Dispute_AUDIO.pkl', 'wb') as Date2:
        pickle.dump(dispute_list, Date2)
    print(' done processing DISPUTE audio ')

if dispute_heatmaps:
    print(' begin DISPUTE heatmaps ')
    dispute_id = 0
    while dispute_id < num_of_disputes:
        with open(f'pickles/NEW_IMP/DISPUTE/{to_load_pickle_date}_all_Dispute_AUDIO.pkl', 'rb') as file2:
            dispute_heatmap_list = pickle.load(file2)
        of_this_dispute = dispute_heatmap_list[dispute_id]
        first_song = of_this_dispute[0]
        second_song = of_this_dispute[1]
        dispute_min_beats = min(len(first_song.eight_beat_groups), len(second_song.eight_beat_groups))
        dispute_corr_matrix = beat_group_corr(first_song, second_song, dispute_min_beats)
        # dispute_corr_matrix = numpy.zeros((dispute_min_beats, dispute_min_beats))
        # for y in range(dispute_min_beats):
            # for x in range(dispute_min_beats):
                # dispute_corr_matrix[x, y] = numpy.corrcoef(first_song.mean_chroma[y], second_song.mean_chroma[x])[0, 1]
        if do_diagonal:
            diag_corr, diag_offset, diag_y_start, diag_y_end, diag_x_start, diag_x_end = (find_diagonal_corr
                                                                                          (dispute_corr_matrix,
                                                                                           dispute_min_beats))
            dispute_diagonal_heatmap(dispute_corr_matrix, dispute_id, round(diag_corr, 4), diag_y_start, diag_x_start,
                                     diag_offset)

            # 10/29 if changed_x:
            extract_dispute_audio(first_song, second_song, diag_y_start, diag_y_end, diag_x_start, diag_x_end,
                                  dispute_min_beats, dispute_id)
            # 10/29 else:
                # 10/29 extract_dispute_audio(first_song, second_song, diag_y_start, diag_y_end, diag_x_start, diag_x_end,
                                      # 10/29 dispute_min_beats, dispute_id)
        # if do_straight:
            # straigt_corr, straight_start, straight_end, dispute_horiz = find_straight_corr(dispute_corr_matrix,
                                                                                           #dispute_min_beats)
        dispute_id = dispute_id + 1
    print(' done processing DISPUTE heatmaps ')


