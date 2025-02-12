
class Song():
    def __init__(self, prompt, student, song, song_audio, song_sr, beat_frames):
        self.prompt = prompt
        self.student = student
        self.song = song
        self.audio = song_audio           # numpy array for WAVE file
        self.has_audio = True
        self.mfcc = None
        self.sr = song_sr
        self.tempo = None
        self.song_chroma = None
        self.beat_frames = beat_frames
        self.beat_mfcc = None
        self.beat_times = None          # numpy array timestamps of song's beats
        self.frame_chromas = None         # contains the mean of chromas of 10 frames after each beat
        self.mean_chroma = []             # contains the mean of chromas of each 8-beat rolling window
        self.eight_beat_groups = []             # new implementation: list of LISTS = each LIST has chromagram of each beat in
                                          # an 8 beat grouping
        # self.wave = None                # name of wav file converted from original mp3 file
        # self.tran_wave = None           # name of transposed wav filed
        self.transposed = False
        self.timbre = None
        self.orig_key = None

    def set_chroma_Song_Data(self, chroma):
        self.song_chroma = chroma

    def set_mfcc_Song_Data(self, mfcc, beat_mfcc):
        self.mfcc = mfcc
        self.beat_mfcc = beat_mfcc

    def set_Title(self, title):
        self.title = title

    def get_Title(self):
        return self.title

    def set_Audio(self, song_audio, song_sr):
        self.audio = song_audio
        self.sr = song_sr
        self.has_audio = True

    def get_Audio(self):
        return self.audio

    def set_SR(self, sr):
        self.sr = sr

    def get_SR(self):
        return self.sr

    def setWaveFile(self, wav):
         self.wave = wav

    def set_Tempo(self, tempo):
        self.tempo = tempo

    def get_Tempo(self):
        return self.tempo

    def set_BeatLocs(self, beat_locs):
        self.beat_locs = beat_locs

    def get_BeatLocs(self):
        return self.beat_locs

    def set_BeatTimes(self, beat_times):
        self.beat_times = beat_times

    def get_BeatTimes(self):
        return self.beat_times

    def set_BeatSec(self, beat_sec):
        self.beatsections = beat_sec

    def get_BeatSec(self):
        return self.beatsections
        # self.onset_str = _onset_s

    def set_WaveFile(self, wavfile):
        self.wave = _wavfile

    def get_WaveFile(self):
        return self.wave

    def set_Timbre(self, timbre):
        self.timbre = timbre

    def get_Timbre(self):
        return self.timbre

    def set_OrigKey(self, key):
        self.orig_key = key

    def get_OrigKey(self):
        return self.orig_key

    def set_SongChroma(self, song_chroma):
        self.song_chroma = song_chroma

    def get_SongChroma(self):
        return self.song_chroma
