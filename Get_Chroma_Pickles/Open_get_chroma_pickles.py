from Global import suno_prompts

from Chroma_Utilities import chroma_of_frames, mean_beat_chroma

from Song_Class import Song

import pickle

import random

prompt = 0
while prompt < suno_prompts:
    print(f" ****** loading next get_chroma pickle for prompt {prompt} ****** ")
    print(' ')
    file_num = random.randint(1, 250)
    file_name = 'file' + str(file_num)
    with open(f'(…your directory path…)/Feb132025_1pm_get_chroma_prompt_{prompt}.pkl', 'rb') as file_name:
        this_prompt_list = pickle.load(file_name)
    student = 0
    for this_student in this_prompt_list:
        current_student = this_student
        song = 0
        while isinstance(current_student[song], Song):
            current_song = current_student[song]
            if current_song.prompt == prompt and current_song.student == student and current_song.song == song:
                print(f"   ---> processing: p {prompt} : st {student}  :  sng {song}")
                print(' ')
                chroma_of_frames(song_for_frames=current_song)
                mean_beat_chroma(rolling_beats_song=current_song)
                current_student[song] = current_song
            song += 1
        student += 1
    with open(f'(....saving updated pickle).save_this_prompt_{prompt}pkl', 'wb') as Date1:
        pickle.dump(this_prompt_list, Date1)
    prompt += 1


