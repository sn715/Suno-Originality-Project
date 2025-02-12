import os

from pathlib import Path

import pickle

from Song_Class import Song

from Dispute_Song_Class import Dispute_Song

import librosa.feature

import numpy

import soundfile


def original_key(song_chroma):
    mean_chroma = numpy.mean(song_chroma, axis=1)
    est_key_index = numpy.argmax(mean_chroma)
    key = notes[est_key_index]
    return key


to_save_pickle_date = 'Aug06'
to_load_pickle_date = 'Aug06'
suno_corr_pickle_date = 'Aug06'
map_date = 'Aug07'
trim = 35
correlation_min = 0.29
beats = 8
num_of_frames = 10


notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
dispute = False
dispute_songs_at = 'all_Dispute_Songs'
num_of_disputes = 8
dispute_heatmaps = True

transpose_list = [[] for _ in range(num_of_disputes)]
print(' begin processing DISPUTE audio')
dispute_root = Path.cwd() / dispute_songs_at
dispute_num = 0
for this_dispute in dispute_root.iterdir():
    songs_iterator = iter(this_dispute.iterdir())
    for this_song in songs_iterator:
        if os.path.isfile(this_song):
            first_audio, first_sr = librosa.load(this_song, sr=None, duration=trim)
            first_cqt_chroma = librosa.feature.chroma_cqt(y=first_audio, sr=first_sr)
            first_song_key = original_key(first_cqt_chroma)
            next_song = next(songs_iterator)
            if os.path.isfile(next_song):
                second_audio, second_sr = librosa.load(next_song, sr=None, duration=trim)
                second_cqt_chroma = librosa.feature.chroma_cqt(y=second_audio, sr=second_sr)
                second_song_key = original_key(second_cqt_chroma)
                if first_song_key != second_song_key:
                    first_key = notes.index(first_song_key)
                    second_key = notes.index(second_song_key)
                    pitch_shift = abs(first_key - second_key)
                    first_audio = librosa.effects.pitch_shift(y=first_audio, sr=first_sr,
                                                              n_steps=float(pitch_shift))
                    soundfile.write(f'{dispute_num}_song_1_transposed.wav', first_audio, first_sr)
                    second_audio = librosa.effects.pitch_shift(y=second_audio, sr=second_sr,
                                                               n_steps=float(0))
                    soundfile.write(f'{dispute_num}_song_2_transposed.wav', second_audio, second_sr)
                    dispute_num = dispute_num + 1
                else:
                    soundfile.write(f'{dispute_num}_song_1_no_transpose.wav', first_audio, first_sr)
                    second_audio = librosa.effects.pitch_shift(y=second_audio, sr=second_sr,
                                                               n_steps=float(0))
                    soundfile.write(f'{dispute_num}_song_2_no_transpose.wav', second_audio, second_sr)
                    dispute_num = dispute_num + 1


