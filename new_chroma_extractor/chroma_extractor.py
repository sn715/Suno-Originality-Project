# python chroma_extractor.py ./input_audio ./output_audio ./output_chroma --n_frames 4 --sr 44100

import os
import argparse
import numpy as np
import librosa
import soundfile as sf

def process_directory(audioDir, audioOut, chromaOut, n_frames=4, sr=44100):
    os.makedirs(audioOut, exist_ok=True)
    os.makedirs(chromaOut, exist_ok=True)

    for fname in os.listdir(audioDir):
        if not fname.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
            continue

        fpath = os.path.join(audioDir, fname)
        print(f"Processing {fpath}...")

        # Load
        y, _ = librosa.load(fpath, sr=sr, mono=True)

        # Beat tracking
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # Chroma
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        beat_chroma = []
        synth_chord = np.zeros_like(y)

        for bt, bf in zip(beat_times, beat_frames):
            frames = chroma[:, bf:bf+n_frames]
            chroma_vec = frames.sum(axis=1)

            if np.sum(chroma_vec) > 0:
                chroma_vec = chroma_vec / np.max(chroma_vec)

            vec = np.concatenate(([bt], chroma_vec))
            beat_chroma.append(vec)

            # chord synthesis
            duration = int(0.25 * sr)
            t = np.linspace(0, 0.25, duration, endpoint=False)
            chord = np.zeros(duration)

            freqs = 261.63 * 2**(np.arange(12)/12.0)
            for i, mag in enumerate(chroma_vec):
                if mag > 0.2:
                    chord += mag * np.sin(2*np.pi*freqs[i]*t)

            start = int(bt*sr)
            end = min(start+duration, len(synth_chord))
            synth_chord[start:end] += chord[:end-start]

        beat_chroma = np.vstack(beat_chroma)

        # Stereo: left=original, right=chord synth
        stereo = np.vstack([y, synth_chord])
        outpath = os.path.join(audioOut, os.path.splitext(fname)[0] + "_beats.wav")
        sf.write(outpath, stereo.T, sr)

        chroma_path = os.path.join(chromaOut, os.path.splitext(fname)[0] + "_chroma.txt")
        np.savetxt(chroma_path, beat_chroma, fmt="%.4f")

        print(f"Saved audio to {outpath}")
        print(f"Saved chroma data to {chroma_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract beat-synchronous chroma and resynthesized audio.")
    parser.add_argument("audioDir", help="Directory of input audio files")
    parser.add_argument("audioOut", help="Directory to write output audio")
    parser.add_argument("chromaOut", help="Directory to write output chroma txt files")
    parser.add_argument("--n_frames", type=int, default=4, help="Number of frames to sum after each beat")
    parser.add_argument("--sr", type=int, default=44100, help="Target sample rate")
    args = parser.parse_args()

    process_directory(args.audioDir, args.audioOut, args.chromaOut, n_frames=args.n_frames, sr=args.sr)
