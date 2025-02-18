
from Song_Class import Song

from Comparison_Class import create_suno_diagonal_compare
                            # suno_straight_compare
                            # plot_heatmap_with_diagonal

from Global import (suno, suno_songs_at, suno_prompts, suno_students, suno_heatmaps_1,
                    suno_heatmaps_2, diag_comparison_list,trim, chroma_analysis, correlation_min,
                    to_save_pickle_date, to_load_pickle_date, do_diagonal, main_id)


from Diagonal_Corr_and_Heatmaps import suno_diagonal_heatmap

# from Straight_Corr_and_Heatmaps import suno_straight_heatmap

from Chroma_Utilities import chroma_of_frames, get_chroma, mean_beat_chroma, beat_group_corr


from Extract_Audio import extract_audio

from pathlib import Path

import re

import os

import random

import pickle

#import librosa.feature
import librosa

import numpy

import math


def sort_and_format_suno_heatmaps():
    over_leaf_1 = r'\item\textit{'
    over_leaf_2 = r'}'
    heatmap_path = r'heatmaps/suno/'
    heat_map_files = os.listdir(heatmap_path)
    for map_file1 in heat_map_files:
        match = re.search(r'(\d+\.\d{1,3})', map_file1)
        if match:
            corr_val1 = match.group(1)
            corr_val2 = float(corr_val1)
            normalized_corr_val = f"{corr_val2:.3f}"
            new_map_file1 = map_file1.replace(corr_val1, normalized_corr_val)
            over_leaf_map_file = over_leaf_1 + new_map_file1 + over_leaf_2
            os.rename(os.path.join(heatmap_path, map_file1), os.path.join(heatmap_path, over_leaf_map_file))
    to_sort = []
    for map_file2 in heat_map_files:
        match = re.search(r'(\d+\.\d{3})', map_file2)
        if match:
            number = float(match.group(1))
            to_sort.append((map_file2, number))
    sort_result = sorted(to_sort, key=lambda x: x[1], reverse=True)
    return sort_result


def detect_remove_duplicates():
    duplicate_counter = 0
    duplicate_path = r'heatmaps/suno/'
    duplicate_files = os.listdir(duplicate_path)
    files_with_stems = {}
    for possible_duplicate in duplicate_files:
        match = re.search(r'_(\d+\.\d{3})_(.+)\.svg$', possible_duplicate)
        if match:
            stem = match.group(1)
            number = float(match.group(2))
            if stem in files_with_stems:
                if number > files_with_stems[stem][1]:
                    os.remove(os.path.join(duplicate_path, files_with_stems[stem][0]))
                    files_with_stems[stem] = (possible_duplicate, number)
                else:
                    os.remove(os.path.join(duplicate_path, possible_duplicate))
                    duplicate_counter = duplicate_counter + 1
            else:
                files_with_stems[stem] = (possible_duplicate, number)

    print('Duplicate files eliminated')
    return duplicate_counter


def get_prompt_list(p_num, a_date):
    print('------------- loading prompt pickle')
    print(' ')
    file_num = random.randint(1, 250)
    file_name = 'file' + str(file_num)
    with open(f'pickles/NEW_IMP/SUNO/{a_date}_{p_num}_prompt_Suno_AUDIO.pkl', 'rb') as file_name:
        temp_list = pickle.load(file_name)
    return temp_list


def compare_across_prompts(list_one, list_two):
    global main_id
    compare_counter2 = 0
    l1 = 0
    while l1 < len(list_one):
        first_student = list_one[l1]
        for first_list_song in first_student:
            l2 = 0
            p1 = first_list_song.prompt + 1
            st1 = first_list_song.student + 1
            sng1 = first_list_song.song + 1
            print(f' ***  Current Song: P {p1}:St {st1}:So:{sng1}')
            while l2 < len(list_two):
                second_student = list_two[l2]
                compare_counter2 = compare_counter2 + len(second_student)
                for second_list_song in second_student:
                    p2 = second_list_song.prompt + 1
                    st2 = second_list_song.student + 1
                    sng2 = second_list_song.song + 1
                    print(f'       Other Song: P {p2}:St {st2}: So {sng2}')
                    shared_length2 = min(len(first_list_song.eight_beat_groups),
                                         len(second_list_song.eight_beat_groups))
                    # corr_matrix2 = numpy.zeros((shared_length2, shared_length2))
                    # for y in range(shared_length2):
                        # for x in range(shared_length2):
                            # corr_matrix2[x, y] = numpy.corrcoef(first_list_song.mean_chroma[y],
                                                                # second_list_song.mean_chroma[x])[0, 1]
                    corr_matrix2 = beat_group_corr(first_list_song, second_list_song, shared_length2)
                    if do_diagonal:
                        # create_suno_diagonal_compare in comparison class
                        diag_comparison2 = create_suno_diagonal_compare(first_list_song, second_list_song,
                                                                            shared_length2, corr_matrix2)
                        diag_comparison2.comp_id = main_id
                        print(f'                 comparison id: {diag_comparison2.comp_id}')
                        print(' ')
                        # if diag_comparison2.d_corr >= correlation_min:
                            # suno_diagonal_heatmap(corr_matrix2, diag_comparison2, main_id)
                            # extract_audio(first_list_song, second_list_song, diag_comparison2, main_id)
                        # else:
                            # print(f'*****  comparison id {diag_comparison2.comp_id} below corr min')
                            # print('')
                        diag_comparison_list.append(diag_comparison2)
                        main_id = main_id + 1
                l2 = l2 + 1
        l1 = l1 + 1
    return compare_counter2


def count_songs_in_prompt(count_list):
    song_total = 0
    st = 0
    while st < len(count_list):
        count_this_student_songs = count_list[st]
        song_total = song_total + len(count_this_student_songs)
        st = st + 1
    return song_total

#most relevant
def compare_within_prompt(prompt_id):
    global main_id
    m = 0
    compare_counter1 = 0
    first_heatmap_list = get_prompt_list(prompt_id, to_load_pickle_date)
    # load pickle list for prompt
    # get_prompt_list function defined above
    #       example:
    #           first_heatmap_list = student_list[  student0[[Song0, Song1],
    #                                               student1[[Song0, Song1],
    #                                               ...
    #                                               student9[[Song0, Song1]  ]
    song_count1 = count_songs_in_prompt(first_heatmap_list)
    # count_songs_in_prompt function defined above
    # song_count1 = total num of songs generated by all students in current prompt
    while m < (len(first_heatmap_list) - 1):
        compare_student = first_heatmap_list[m]
        # extract a student list of songs
        #   example:
        #       first_heatmap_list[0]
        #               compare_student = student0[[Song0, Song1]
        #       first_heatmap_list[1]
        #               compare_student = student1[[Song0, Song1]
        for compare_song in compare_student:
            # compare_song = Song Class object in compare_student list
            st1 = compare_song.student + 1
            # student ID + 1 for readability purposes
            sg1 = compare_song.song + 1
            # song ID + 1 for readability purposes
            print(f'----- current student: {st1} // song: {sg1} ')
            print('       in same prompt with....')
            ahead = m + 1
            # ahead var acts as an index of the next student in first_heatmap_list
            while ahead < len(first_heatmap_list):
                # condition states that ahead cannot exceed length of first_heatmap_list
                next_student = first_heatmap_list[ahead]
                # example:
                #   compare_student = student5[[Song0, Song1]
                #   next_student    = student6[[Song0, Song1]
                compare_counter1 = compare_counter1 + len(next_student)
                # compare_counter1 is incremented each time a song from a student list is compared
                # to a song from a song from a different student's list
                #   therefore:
                #           compare_counter1 represents the total number of song pair comparisons
                #           executed within the same prompt
                for other_song in next_student:
                    # other_song  = Song Class object in next_student list
                    st2 = other_song.student + 1
                    # student ID + 1 for readability purposes
                    sg2 = other_song.song + 1
                    # song ID + 1 for readability purposes
                    print(f'   ..... other student: {st2} // song: {sg2}  ')
                    shared_length1 = min(len(compare_song.eight_beat_groups), len(other_song.eight_beat_groups))
                    # since each Song will have diff num of audio frames, then each Song will have diff 8-beat groups
                    #   therefore:
                    #       determine which of the 2 songs being compared has the min num of 8-beat groups
                    # ///corr_matrix1 = numpy.zeros((shared_length1, shared_length1))
                    # ///for y in range(shared_length1):
                        # ///for x in range(shared_length1):
                            # ///corr_matrix1[x, y] = numpy.corrcoef(compare_song.mean_chroma[y],
                                                                # vvvother_song.mean_chroma[x])[0, 1]
                    corr_matrix1 = beat_group_corr(compare_song, other_song, shared_length1)
                    # beat_group_corr function defined in Chroma_Utilities.py
                    if do_diagonal:
                        # do_diagonal is a global var from Global.py
                        diag_comparison1 = create_suno_diagonal_compare(compare_song, other_song, shared_length1,
                                                                        corr_matrix1)
                        # create_suno_diagonal_compare function defined in Comparison_Class.py
                        # returns a Diagonal Class object
                        diag_comparison1.comp_id = main_id
                        # give the newly created Diagonal Class object the unique ID
                        # main_id is a unique id for each unique song pair comparison
                        if diag_comparison1.d_corr >= correlation_min:
                            # if highest 8-beat diagonal correlation is >= similarity threshold
                            # then generate a heatmap to visualize the comparison of these 2 songs
                            suno_diagonal_heatmap(corr_matrix1, diag_comparison1, main_id)
                            # suno_diagonal_heatmap function defined in Diagonal_Corr_and_Heatmaps.py
                            extract_audio(compare_song, other_song, diag_comparison1, main_id)
                            #  extract_audio function defined in Extract_Audio.py
                        else:
                            print(f'*****  comparison id {diag_comparison1.comp_id} below corr min')
                            print('')
                        diag_comparison_list.append(diag_comparison1)
                        main_id = main_id + 1

                print(f'   ............. {compare_counter1} comparisons in prompt {prompt_id} so far ')
                ahead = ahead + 1
        m = m + 1
    return song_count1, compare_counter1


# ----------------------------------
# STAGE 1
#   BEGIN PROCESSING SUNO SONG AUDIO
# ----------------------------------
if suno:
    # suno is a global var from Global.py
    print(' begin processing SUNO audio')
    suno_root = Path.cwd() / suno_songs_at
    # suno_songs_at is a global var from Global.py
    # suno_songs_at represents the name of main folder
    #       each prompt sub-folder has 11 student sub-folders
    #               each student sub-folder has 2-4 suno song files
    prompt = 0
    for this_prompt in suno_root.iterdir():
        # access prompt sub-folder
        student = 0
        student_list = [[] for _ in range(suno_students)]
        # suno_students is a global var from Global.py
        # initializes student_list as a list of empty lists
        for this_student in this_prompt.iterdir():
            # access student sub-folder in prompt sub-folder
            current_student = student_list[student]
            # student var acts as an index value
            # examples:
            #       current_student = address of an empty list
            #           current_student = student_list[0]
            #               current_student = student_list[1]
            #                   current_student = student_list[2]
            song = 0
            for audio_file in this_student.iterdir():
                # access song sub-folder in student sub-folder
                if os.path.isfile(audio_file):
                    # if there is a file = true
                    audio, sr = librosa.load(audio_file, sr=None, duration=trim)
                    # trim (35 secs) is global var from Global.py
                    # load first 35 secs of song audio file
                    # returns audio --> a numpy array of floating point nums
                    tempo, beat_frames = librosa.beat.beat_track(y=audio, sr=sr)
                    # beat_frames is an array of frame indices where detected beats occur
                    # examples
                    #       beat_frames[10, 13, 27,.... ] =
                    #           beat_frames[0] = 10 (audio frame at index 10)
                    #           beat_frames[1] = 13 (audio frame at index 13)
                    # the audio frames are in the audio numpy array returned by librosa.load:
                    #           audio[frame0, frame1, frame2, frame3...]
                    print(f'prompt: {prompt}  student: {student}  song: {song} ')
                    current_song = Song(prompt, student, song, song_audio=audio, song_sr=sr, beat_frames=beat_frames)
                    # initiate new Song class object
                    #   store prompt ID, student ID, song ID, song's audio numpy array, sr, beat frames array
                    if chroma_analysis:
                        # chroma_analysis is global var from Global.py
                        # get_chroma, chroma_of_frames, mean_beat_chroma functions below
                        #   defined in Chroma_Utilities.py
                        get_chroma(song_for_chroma=current_song)
                        chroma_of_frames(song_for_frames=current_song)
                        mean_beat_chroma(rolling_beats_song=current_song)
                    current_student.append(current_song)
                    # add current_song Song Class object to current_student list
                    #   therefore:
                    #       each index in current_student list holds a Song Class object
                    #       example:
                    #           current_student[Song0, Song1, Song2...]
                song = song + 1
            student = student + 1
        print('')
        with open(f'pickles/NEW_IMP/SUNO/{to_save_pickle_date}_{prompt}_prompt_Suno_AUDIO.pkl', 'wb') as Date1:
            pickle.dump(student_list, Date1)
            # to_save_pickle_date is a global var from Global.py
            #
            # save student_list in a pickle file for each prompt
            #   example:
            #       prompt 0 pickle = student_list[  student0[[Song0, Song1],
            #                                        student1[[Song0, Song1],
            #                                        ...
            #                                        student9[[Song0, Song1]  ]
            #
            #       prompt 1 pickle = student_list[  student0[[Song0, Song1],
            #                                        student1[[Song0, Song1],
            #                                        ...
            #                                        student9[[Song0, Song1]  ]
        prompt = prompt + 1
    print(' done processing SUNO audio ')

# ----------------------------------
# STAGE 2
#   COMPARE SONG PAIRINGS TO DETERMINE IF THERE ARE 8-BEATS >= correlation_min global var
#   GENERATE HEATMAPS FOR SONG PAIRINGS
# ----------------------------------
if suno_heatmaps_1:
    # sun_heatmaps_1 is a global var in Global.py
    #   this loop compares song pairs that have the same prompt ID
    print(' begin SUNO heatmaps part 1 ')
    pid1 = 0
    # pid1 is a prompt counter
    inner_comps = 0
    cross_comps = 0
    total_comps = 0
    songs_counted = 0
    duplicates = 0
    total_songs = 0
    while pid1 < suno_prompts:
        # suno_prompts = 8, global var in Global.py
        display_id1 = pid1 + 1
        # prompt ID + 1 for readability purposes
        #   if pid1 = 0, it will be printed out as Prompt 1
        #   if pid1 = 5, it will be printed out as Prompt 6
        print(f'---------- ')
        print(f'current prompt = {display_id1}')
        print(f'---------- ')
        songs_counted, inner_comps = compare_within_prompt(pid1)
        # call compare_within_prompt function defined above
        total_comps = total_comps + inner_comps
        print(f'---- {songs_counted} songs in this prompt')
        print('')
        total_songs = total_songs + songs_counted
        pid1 = pid1 + 1
    with open(f'pickles/NEW_IMP/SUNO/{to_save_pickle_date}_all_inner_prompt_comps_Suno_AUDIO.pkl', 'wb') as Date6:
        pickle.dump(diag_comparison_list, Date6)
    print('')
    print(' ************************************************* ')
    print('       INNER PROMPT COMPARISONS COMPLETE  ')
    print(' ************************************************** ')
    print('')

if suno_heatmaps_2:
    # sun_heatmaps_2 is a global var in Global.py
    #   this loop compares song pairs that have the diff prompt ID
    main_id = 2141
    total_comps = 2141
    print(' begin SUNO heatmaps part 2 ')
    diag_comparison_list = []
    pid2 = 0
    print('')
    print(' ************************************************* ')
    print('       BEGIN CROSS PROMPT COMPARISONS  ')
    print(' ************************************************** ')
    print('')
    while pid2 < (suno_prompts-1):
        # loop for comparing a song against all songs in other prompts
        first_list = get_prompt_list(pid2, to_load_pickle_date)
        next_prompt = pid2 + 1
        if pid2 < next_prompt:
            display_id1 = pid2 + 1
            while next_prompt < suno_prompts:
                display_id2 = next_prompt + 1
                print('                           //////')
                print(f'                          P {display_id1} x P {display_id2}')
                print('                           //////')
                print(' ')
                second_list = get_prompt_list(next_prompt, to_load_pickle_date)
                cross_comps = compare_across_prompts(first_list, second_list)
                total_comps = total_comps + cross_comps
                next_prompt = next_prompt + 1
        pid2 = pid2 + 1
    print(f'total num of comparisons: {total_comps}')
    print(f'total num of songs: {total_songs}')
    if do_diagonal:
        with open(f'pickles/NEW_IMP/SUNO/{to_save_pickle_date}_all_cross_prompt_comps_Suno_AUDIO.pkl', 'wb') as Date7:
            pickle.dump(diag_comparison_list, Date7)
    print(' done creating SUNO heatmaps ')
