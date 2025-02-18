from Song_Class import Song

#from Dispute_Song_Class import Dispute_Song

from Global import beats, num_of_frames

import librosa.feature

import numpy


def get_chroma(song_for_chroma):
    # song_for_chroma = Song Class object passed in as parameter
    cqt_chroma = librosa.feature.chroma_cqt(y=song_for_chroma.audio, sr=song_for_chroma.sr)
    # chroma_cqt is a NumPy array where each column represents a chroma feature vector for
    #       a specific audio frame in the NumPy array of frames --> song_for_chroma.audio
    # chroma_cqt is a 12-dimensional vector representing relative energy of each pitch class in an audio frame
    #       Rows(12 total) represent the 12 pitch classes(C, D, ..., B).
    #       Columns(T total) represent time frames in the song_for_chroma.audio
    #
    #       Here is a truncated visual representation:
    #
    #            frame1   frame2   frame3 .....
    #       C       .21
    #       c#      .05
    #       D       .33
    #       d#      .1
    #       E
    #       F
    #
    # chroma_cqt[:, 1] returns the chromagram of first frame
    # chroma_cqt[:, 3] returns the chromagram of third frame
    song_for_chroma.set_chroma_Song_Data(chroma=cqt_chroma.T)
    # transpose the cqt_chroma 2dim Numpy array
    # store the transposed cqt_chroma at chroma property of song_for_chroma Song Class object
    # visual representation:
    #    transposed cqt_chroma stored at chroma (num of frames 'f' x 12):
    #    [ [ C_1, C#_1, D_1, D#_1, E_1, F_1, F#_1, G_1, G#_1, A_1, A#_1, B_1 ],
    #      [ C_2, C#_2, D_2, D#_2, E_2, F_2, F#_2, G_2, G#_2, A_2, A#_2, B_2 ]
    #        ...
    #      [ C_f, C#_f, D_f, D#_f, E_f, F_f, F#_f, G_f, G#_f, A_f, A#_f, B_f ]  ]
    #
    print(f' --- size of transposed chroma: {song_for_chroma.song_chroma.shape}')
    print(f' ----- size of beat frames: {song_for_chroma.beat_frames.shape}')
    # both sizes should be the same and equal the same number of frames
    return


# chroma_of_frames function calculates the avg chromagram of each 10 audio frame set where
#   the 1st audio frame for any set is an audio frame with a detected beat and the
#   other 9 audio frames are those 9 audio frames that occur immediately after that
#   1st audio frame
def chroma_of_frames(song_for_frames):
    # song_for_frames = Song Class object passed in as parameter
    frame_groups_for_beats = []
    # initialize empty list
    for beat_frame_index in song_for_frames.beat_frames:
        # gets frame index of each audio frame with a detected beat
        start = beat_frame_index
        end = start + num_of_frames
        # num_of_frames = 10, is a global var from Global.py
        if end <= song_for_frames.song_chroma.shape[0]:
            # true when end is <= the total num of frames in song_chroma property
            #   (i.e. transposed chroma_cqt)
            frame_group = song_for_frames.song_chroma[start:end, :]
            # access the transposed chroma_cqt stored at chroma property of song_for_frames Song
            #   Class object
            # frame_group holds chroma for 10 audio frames
            mean_of_frame_group = numpy.mean(frame_group, axis=0)
            # mean_of_frame_group = mean chromagram value of the current 10 audio frame set
            #   mean_of_frame_group =
            #   [  mean(C_1, C_2, ..., C_10),
            #      mean(C#_1, C#_2, ..., C#_10),
            #      mean(D_1, D_2, ..., D_10),
            #      mean(D#_1, D#_2, ..., D#_10),
            #      mean(E_1, E_2, ..., E_10),
            #      mean(F_1, F_2, ..., F_10),
            #      mean(F#_1, F#_2, ..., F#_10),
            #      mean(G_1, G_2, ..., G_10),
            #      mean(G#_1, G#_2, ..., G#_10),
            #      mean(A_1, A_2, ..., A_10),
            #      mean(A#_1, A#_2, ..., A#_10),
            #      mean(B_1, B_2, ..., B_10) ]
            frame_groups_for_beats.append(mean_of_frame_group)
            #   when the IF loop terminates:
            #       each index of frame_groups_for_beats list holds an avg chromagram value of 10
            #       audio frames -->
            #           each beat is represented as: [avg_C, avg_C#, avg_D,...., avg_B]
        song_for_frames.frame_chromas = frame_groups_for_beats
        # store frame_groups_for_beats list at frame_chromas property
    print(f' ----- size of mean of frames for each beat: {len(song_for_frames.frame_chromas)}')
    # len(song_for_frames.frame_chromas) should = total num of frames in beat_frames property
    return


# mean_beat_chroma function calculates the avg chromagram of a rolling 8-beat window
#   each beat is represented by an avg chroma of 10 audio frames calculated
#   by the chroma_of_frames function above
def mean_beat_chroma(rolling_beats_song):
    # rolling_beats_song = Song Class object passed in as parameter
    for beat in range(len(rolling_beats_song.beat_frames)):
        if (beat + beats) < len(rolling_beats_song.beat_frames):
            # beats = 8, is a global var from Global.py
            start = beat
            end = beat + beats
            beat_window = rolling_beats_song.frame_chromas[start:end]
            # beat_window = list of current 8-beat group extracted from frame_chromas property
            #   that is determined by the chroma_of_frames function above
            #       frame_chromas = list of avg chroma of each 10 audio frame set
            #       therefore:
            #           each index in beat_window is an avg chroma of a 10 audio frame set
            #               beat_window = [avg_chroma_1, avg_chroma_2, ..., avg_chroma_8],
            #                               where each avg_chroma_i is a 12-dimensional array
            #                               such as [10_frames_mean_C, 10_frames_mean_C#,..., 10_frames_mean_B]
            rolling_beats_song.eight_beat_groups.append(beat_window)
            # //new implementation
            # add current beat_window list to eight_beat_groups list property
            mean_of_beat_window = numpy.mean(beat_window, axis=0)
            # mean_of_beat_window = mean chromagram value of the extracted 8-beat group
            #   for beats 0 to 7:
            #       --> [mean(C0...C7), mean(C#0...C#7),..., mean(B0...B7)]
            rolling_beats_song.mean_chroma.append(mean_of_beat_window)
            # //old implementation
            # add mean chromagram value of the extracted 8-beat group to mean_chroma list property
    return

"""
def beat_group_corr(this_compare_song, this_other_song, length):
    # the 2 songs that are being compared are passed in parameters
    # length var parameter represents the num of 8-beat groups
    beat_group_avg_corr_matrix = numpy.zeros((length, length))
    # initialize a 2-dimensional NumPy array filled with zeros
    #   visual representation:
    #       where length = 5 (i.e. both songs have five 8-beat groups)
    #           beat_group_avg_corr_matrix([ [0., 0., 0., 0., 0.],
    #                                        [0., 0., 0., 0., 0.],
    #                                        [0., 0., 0., 0., 0.],
    #                                        [0., 0., 0., 0., 0.],
    #                                        [0., 0., 0., 0., 0.] ])
    for y in range(length):
        # this loop compares each 8-beat group from song 1 with each 8-beat group of song 2
        # remember that:
        #       each index of eight_beat_groups property is a list of 8 beats
        #        --> eight_beat_groups[index] = [avg_chroma_1, avg_chroma_2, ..., avg_chroma_8],
        #                                    where each avg_chroma_i is a 12-dimensional array
        #                                    such as [10_frames_mean_C, 10_frames_mean_C#,..., 10_frames_mean_B]
        current_chroma_group = this_compare_song.eight_beat_groups[y]
        # current_chroma_group = [avg_chroma_1, avg_chroma_2, ..., avg_chroma_8]
        for x in range(length):
            other_chroma_group = this_other_song.eight_beat_groups[x]
            # other_chroma_group = [avg_chroma_1, avg_chroma_2, ..., avg_chroma_8]
            chroma_group_corr = []
            for z in range(beats):
                # beats = 8, is a global var from Global.py
                current_chroma = current_chroma_group[z]
                # current_chroma is a 12-dimensional array
                #   such as beat --> [10_frames_mean_C, 10_frames_mean_C#,..., 10_frames_mean_B]
                other_chroma = other_chroma_group[z]
                # other_chroma is a 12-dimensional array
                #   such as beat --> [10_frames_mean_C, 10_frames_mean_C#,..., 10_frames_mean_B]
                flat_current = current_chroma.flatten()
                #  //not sure if this flatten() call is needed
                flat_other = other_chroma.flatten()
                #  //not sure if this flatten() call is needed
                chroma_corr_matrix = numpy.corrcoef(flat_current, flat_other)
                # compute correlations of chromagrams of two 8-beat groups
                current_chroma_corr = chroma_corr_matrix[0, 1]
                chroma_group_corr.append(current_chroma_corr)
                # chroma_group_corr will end up as a list of 8 correlation values for z  = 0 to 8
            beat_group_avg_corr = numpy.mean(chroma_group_corr)
            # calculate avg correlation value for this pair of 8-beat groups
            beat_group_avg_corr_matrix[y][x] = beat_group_avg_corr
            # store avg correlation value in matrix
    return beat_group_avg_corr_matrix
"""


def beat_group_corr(this_compare_song, this_other_song, length):
    # Initialize a 2-dimensional NumPy array filled with zeros
    beat_group_avg_corr_matrix = numpy.zeros((length, length))

    for y in range(length):
        # Get the current 8-beat group from the first song
        current_chroma_group = this_compare_song.eight_beat_groups[y]
        
        for x in range(length):
            # Get the corresponding 8-beat group from the second song
            other_chroma_group = this_other_song.eight_beat_groups[x]
            
            # List to store correlations for each corresponding beat pair
            chroma_group_corr = []
            
            for z in range(beats):
                # Get the chromagram for the current beat in both groups
                current_chroma = current_chroma_group[z]
                other_chroma = other_chroma_group[z]
                
                # Compute the correlation between the two chromagrams
                chroma_corr_matrix = numpy.corrcoef(current_chroma, other_chroma)
                current_chroma_corr = chroma_corr_matrix[0, 1]
                
                # Store the correlation for this corresponding beat pair
                chroma_group_corr.append(current_chroma_corr)
            
            # Average the correlations for the 8 corresponding beat pairs
            beat_group_avg_corr = numpy.mean(chroma_group_corr)
            
            # Store the average correlation in the matrix
            beat_group_avg_corr_matrix[y][x] = beat_group_avg_corr
    
    return beat_group_avg_corr_matrix


