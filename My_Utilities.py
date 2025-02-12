import sounddevice as sd

import numpy


from IPython.display import Audio


def index_of(x):
    return x-1


def init_matrix(song_root):
    max_songs = 0
    max_students = 0
    max_prompts = 0
    students = 0
    songs = 0
    for prompt_folder in song_root.iterdir():
        # if prompt_folder.is_dir():
        students, songs = get_max_of(prompt_folder)
        if students > max_students:
            max_students = students
        if songs > max_songs:
            max_songs = songs
        max_prompts = max_prompts + 1
    return [[[] for _ in range(max_students)] for _ in range(max_prompts)], max_prompts, max_students, max_songs
    # return ([[[None] * max_songs for _ in range(max_students)] for _ in range(max_prompts)], max_prompts,
    # max_students, max_songs)


def get_max_of(current_prompt):
    student_counter = 0
    for student in current_prompt.iterdir():
        song_counter = 0
        for song in student.iterdir():
            song_counter = song_counter + 1
        student_counter = student_counter + 1
    return student_counter, song_counter


def play_song(_pid, _sid, _matrix):
    print(' ********* ')
    print('...playing song...')
    sd.default.device = 1, 6
    song_nump_arr = _matrix[index_of(_pid)][index_of(_sid)].get_AudioArr()
    samp_rate = _matrix[index_of(_pid)][index_of(_sid)].get_SR()
    sd.play(song_nump_arr, samplerate=samp_rate)
    duration = len(song_nump_arr) / samp_rate
    sd.sleep(int(duration * 1000))
    print('...song finished...')
    print(' ******** ')
    return


def print_song(matrix, pid, sid):
    current_song = get_song(matrix, pid, stid, soid)
    print(' _____ song data  _____')
    print(f'Prompt ID is {current_song.pid} : '
          f'Student ID is {current_song.stid} : '
          f'Song ID is {current_song.soid}')
    print(f'Song Title is: {current_song.title} ')
    print(f'Original Key: {current_song.orig_key}')
    print(f'Song transposed? {current_song.transposed}')
    print('')
    print(f'Song Numpy Array: {current_song.audio}')
    print(f'    ---> shape of song numpy array: {current_song.audio.shape}')
    print(' ')
    print(' _____ beats data _____')
    print(f'    ---> Tempo = {current_song.tempo}')
    print(f'    ---> Beat Locs at {current_song.beat_locs}')
    print(f'    ---> shape of beat locations array: {current_song.beat_locs.shape}')
    print(' ')
    print(f'    ---> Beat Times at{current_song.beat_times}')
    print(f'    ---> shape of beat times array:{current_song.beat_times.shape}')
    print(' ')
    print(' _____ timbre data _____')
    print(f'    ---> Timbre = {current_song.timbre}')
    print(' ')
    return


def print_chroma(mean_beat_matrix, currentsong, pid, sid):
    print(' _____ CHROMA data  _____')
    print(f'Prompt ID is {currentsong.pid} : '
          f'Song ID is {currentsong.sid}')
    print(f'Song Title is: {currentsong.title} ')
    print('')
    print(f' *** Song Chromagram:  {currentsong.song_chroma}')
    print('')
    print(f' *** Chroma Over Frames (List of Arrays [12 pitches per FRAME]):  ')
    print(currentsong.beat_chroma)
    print('')
    print(f' *** Mean Chroma Per Beat (List of Arrays [12 pitches per BEAT]):  ')
    print(f'     // mean of chromas in 8 beat windows // ')
    print('')
    print(mean_beat_matrix[index_of(pid)][index_of(sid)])
    print('')
    print(' __________')
    print('')


def get_song(matrix, pid, studentid, songid):
    current_song = matrix[index_of(pid)][index_of(studentid)][index_of(songid)]
    return current_song


def print_song_group(matrix, p_max, s_max):
    for p in range(p_max):
        xid = p + 1
        for s in range(s_max):
            yid = s + 1
            print_song(matrix, xid, yid)


def print_chroma_data(_matrix, _p, _s):
    tempSong = _matrix[index_of(_p)][index_of(_s)]
    print('')
    print(' ....chroma data....  ')
    print('')
    print(f'Prompt ID is {tempSong.prompt} : ')
    print(f'Song ID is {tempSong.song}')
    print(f'Song Title is: {tempSong.title} ')
    print(f'        ---> shape of beat times array:{tempSong.beat_times.shape}')
    print(' ')
    print(f'        ---> length of chroma array: {len(tempSong.beat_chrom)}')
    print(' ')


def print_length_mean_successive_chroma(_matrix, _p, _s):
    print(f'        ---> length of successive window chroma array: {len(_matrix[index_of(_p)][index_of(_s)])}')
    print(' ')
    print(' ----- ')
    print(' ----- ')
    print(' ')