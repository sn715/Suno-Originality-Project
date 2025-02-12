class Dispute_Song():
    def __init__(self, dispute, song, song_audio, song_sr, beat_frames):
        self.dispute = dispute
        self.song = song
        self.audio = song_audio  # numpy array for WAVE file
        self.has_audio = True
        self.mfcc = None
        self.sr = song_sr
        self.song_chroma = None
        self.tempo = None
        self.beat_frames = beat_frames
        self.beat_mfcc = None
        self.beat_times = None  # numpy array timestamps of song's beats
        self.frame_chromas = None         # contains the mean of chromas of 10 frames after each beat
        self.mean_chroma = []             # contains the mean of chromas of each 8-beat rolling window
        self.eight_beat_groups = []  # new implementation: list of LISTS = each LIST has chromagram of each beat in
                                     # an 8 beat grouping

    def set_chroma_Song_Data(self, chroma):
        self.song_chroma = chroma

    def set_Dispute_Song_Data(self, audio, sr, mfcc, tempo, beat_frames, beat_mfcc):
        self.audio = audio
        self.sr = sr
        self.has_audio = True
        self.mfcc = mfcc
        self.tempo = tempo
        self.beat_frames = beat_frames
        self.beat_mfcc = beat_mfcc
