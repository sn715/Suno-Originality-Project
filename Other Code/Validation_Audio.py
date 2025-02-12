from Dispute_Song_Class import Dispute_Song

from Global import (validate, validate_songs_at, num_of_validations, validate_heatmaps,
                    chroma_analysis, trim, to_save_pickle_date, to_load_pickle_date, do_diagonal,
                    do_straight)

from Diagonal_Corr_and_Heatmaps import find_diagonal_corr, validate_diagonal_heatmap

from Chroma_Utilities import chroma_of_frames, get_chroma, mean_beat_chroma, beat_group_corr

from pathlib import Path

import os

import pickle

import librosa.feature

import numpy


if validate:
    valid_list = [[] for _ in range(num_of_validations)]
    print(' begin processing VALIDATE audio')
    valid_root = Path.cwd() / validate_songs_at
    valid_num = 0
    for this_pair in valid_root.iterdir():
        valid_list[valid_num] = []
        current_validation = valid_list[valid_num]
        song = 0
        for song_to_validate in this_pair.iterdir():
            print(f'validation: {valid_num}  song: {song} ')
            if os.path.isfile(song_to_validate):
                audio, sr = librosa.load(song_to_validate, sr=None, duration=trim)
                tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
                valid_song = Dispute_Song(valid_num, song, song_audio=audio, song_sr=sr, beat_frames=beat_frames)
                if chroma_analysis:
                    get_chroma(song_for_chroma=valid_song)
                    chroma_of_frames(song_for_frames=valid_song)
                    mean_beat_chroma(rolling_beats_song=valid_song)
                current_validation.append(valid_song)
                song = song + 1
        valid_num = valid_num + 1
        print('')
    with open(f'pickles/NEW_IMP/VALIDATE/{to_save_pickle_date}_all_Validate_AUDIO.pkl', 'wb') as Date3:
        pickle.dump(valid_list, Date3)
    print(' done processing VALIDATE audio ')

if validate_heatmaps:
    print(' begin VALIDATE heatmaps ')
    with open(f'pickles/NEW_IMP/VALIDATE/{to_load_pickle_date}_all_Validate_AUDIO.pkl', 'rb') as file3:
        valid_heatmap_list = pickle.load(file3)
    valid_id = 0
    while valid_id < num_of_validations:
        this_validation = valid_heatmap_list[valid_id]
        first_valid_song = this_validation[0]
        second_valid_song = this_validation[1]
        print(f'{first_valid_song.dispute} : {first_valid_song.song}')
        print(f'{second_valid_song.dispute} : {second_valid_song.song}')
        print('--xx--')
        valid_min_beats = min(len(first_valid_song.eight_beat_groups), len(second_valid_song.eight_beat_groups))

        valid_corr_matrix = beat_group_corr(first_valid_song, second_valid_song, valid_min_beats)
        # valid_corr_matrix = numpy.zeros((valid_min_beats, valid_min_beats))
        # for y in range(valid_min_beats):
            # for x in range(valid_min_beats):
                # valid_corr_matrix[x, y] = numpy.corrcoef(first_valid_song.mean_chroma[y],
                                                           # second_valid_song.mean_chroma[x])[0, 1]
        if do_diagonal:
            valid_corr, valid_offset, valid_start, valid_end, other_start, other_end = (find_diagonal_corr
                                                                                         (valid_corr_matrix,
                                                                                          valid_min_beats))
            validate_diagonal_heatmap(valid_corr_matrix, valid_id, round(valid_corr, 4), valid_offset,
                                      valid_start, valid_end, valid_min_beats)
        # if do_straight:
        valid_id = valid_id + 1
        print(valid_id)
    print(' done processing VALIDATE heatmaps ')