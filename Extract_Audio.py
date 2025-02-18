from Song_Class import Song

from Comparison_Class import Comparison

#from Dispute_Song_Class import Dispute_Song

from Diagonal_Corr_and_Heatmaps import dispute_heatmap_labels

import librosa

import soundfile as sf

from Global import audio_date, beats

import os


# the extract_audio function receives 2 songs that have been compared and extracts audio from both,
# the extracted audio are the highest correlated 8-beats from each song
def extract_audio(song_y, song_x, curr_comparison, extract_id):  #removed last param: compare_num
    cc = curr_comparison
    audio_y = song_y.audio
    frames_y = song_y.beat_frames[:cc.length]
    audio_x = song_x.audio
    frames_x = song_x.beat_frames[:cc.length]

    # 10/29 if cr.offset < 0:
        # 10/29 start_y = cr.y_start + abs(cr.offset)
        # 10/29 end_y = start_y + beats
        # 10/29 start_x = cr.x_start
        # 10/29 end_x = cr.x_end
    # 10/29 else:
        # 10/29 start_y = cr.y_start
        # 10/29 end_y = cr.y_end
        # 10/29 start_x = cr.x_start
        # 10/29 end_x = cr.x_end

    start_time_y = librosa.frames_to_time(frames_y[cc.y_start], sr=song_y.sr)
    if cc.y_end >= len(frames_y):
        end_time_y = librosa.frames_to_time(frames_y[-1], sr=song_y.sr)
    else:
        end_time_y = librosa.frames_to_time(frames_y[cc.y_end], sr=song_y.sr)

    start_time_x = librosa.frames_to_time(frames_x[cc.x_start], sr=song_x.sr)
    if cc.x_end >= len(frames_x):
        end_time_x = librosa.frames_to_time(frames_x[-1], sr=song_x.sr)
    else:
        end_time_x = librosa.frames_to_time(frames_x[cc.x_end], sr=song_x.sr)

    extract_y = audio_y[int(start_time_y * song_y.sr):int(end_time_y * song_y.sr)]
    extract_x = audio_x[int(start_time_x * song_x.sr):int(end_time_x * song_x.sr)]
    prefix = f'{cc.d_corr}__{extract_id}_'
    file_y, file_x, basedir = get_extract_title(song_y, song_x, prefix)
    sf.write(file_y,  extract_y, song_y.sr)
    sf.write(file_x,  extract_x, song_x.sr)
    cc.x_extract = extract_x
    cc.y_extract = extract_y
    # 10/29  if cr.offset > 0:
        # 10/29 start_x2 = start_y + cr.offset
        # 10/29 end_x2 = start_x2 + beats
        # 10/29 xpid = song_x.prompt + 1
        # 10/29 xstdid = song_x.student + 1
        # 10/29  xsngid = song_x.song + 1
        # 10/29 offset_file = prefix + f'___P{xpid}_St{xstdid}_Sng{xsngid}' + 'offset_extract' + '.wav'
        # 10/29 get_offset_x_extract(start_x2, end_x2, frames_x, song_x, os.path.join(basedir, offset_file))
    return


def get_offset_x_extract(offset_start, offset_end, x_frames, x_song, offset_file):
    x_audio = x_song.audio
    x_sr = x_song.sr
    if offset_end >= len(x_frames):
        offset_end_time = librosa.frames_to_time(x_frames[-1], sr=x_sr)
    else:
        offset_end_time = librosa.frames_to_time(x_frames[offset_end], sr=x_sr)
    offset_start_time = librosa.frames_to_time(x_frames[offset_start], sr=x_sr)
    offset_extract = x_audio[int(offset_start_time * x_sr):int(offset_end_time * x_sr)]
    sf.write(offset_file, offset_extract, x_sr)
    return


def get_extract_title(ysong, xsong, p_fix):  # removed last param: c_num
    yp = ysong.prompt + 1
    yst = ysong.student + 1
    ysg = ysong.song + 1
    y_file = p_fix + f'_P{yp}_St{yst}_Sng{ysg}' + 'Y_extract' + '.wav'

    xp = xsong.prompt + 1
    xst = xsong.student + 1
    xsg = xsong.song + 1
    x_file = p_fix + f'_P{xp}_St{xst}_Sng{xsg}' + 'X_extract' + '.wav'

    base_dir = f'pickles/NEW_IMP/SUNO/extract_audio/{audio_date}/{yp}P_v_{xp}P'
    os.makedirs(base_dir, exist_ok=True)

    return os.path.join(base_dir, y_file), os.path.join(base_dir, x_file), base_dir


def extract_dispute_audio(ysong, xsong, ystart, yend, xstart, xend, dispute_length, did):

    frames_y = ysong.beat_frames[:dispute_length]
    frames_x = xsong.beat_frames[:dispute_length]

    start_time_y = librosa.frames_to_time(frames_y[ystart], sr=ysong.sr)
    if yend >= len(frames_y):
        end_time_y = librosa.frames_to_time(frames_y[-1], sr=ysong.sr)
    else:
        end_time_y = librosa.frames_to_time(frames_y[yend], sr=ysong.sr)

    start_time_x = librosa.frames_to_time(frames_x[xstart], sr=xsong.sr)
    if xend >= len(frames_x):
        end_time_x = librosa.frames_to_time(frames_x[-1], sr=xsong.sr)
    else:
        end_time_x = librosa.frames_to_time(frames_x[xend], sr=xsong.sr)

    segment_y = ysong.audio[int(start_time_y * ysong.sr):int(end_time_y * ysong.sr)]
    segment_x = xsong.audio[int(start_time_x * xsong.sr):int(end_time_x * xsong.sr)]

    title_y, title_x = get_dispute_segment_title(ysong, xsong, did)
    sf.write(title_y,  segment_y, ysong.sr)
    sf.write(title_x,  segment_x, xsong.sr)
    return


def get_dispute_segment_title(yso, xso, d_id):
    full_title, song_of_y, song_of_x = dispute_heatmap_labels(d_id)
    y_title = f'pickles/NEW_IMP/DISPUTE/audio_extracts/{d_id}_' + song_of_y + 'extract' + audio_date + '.wav'
    x_title = f'pickles/NEW_IMP/DISPUTE/audio_extracts/{d_id}_' + song_of_x + 'extract' + audio_date + '.wav'
    return y_title, x_title
