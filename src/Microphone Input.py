import sounddevice as sd
import numpy as np
import librosa
import time

# Audio settings
SAMPLE_RATE = 44100
CHANNELS = 1
UPDATE_RATE = 5  # times per second
CHUNK_DURATION = 1.0 / UPDATE_RATE  # seconds

def get_volume(y):
    return np.linalg.norm(y) * 10

def get_pitch(y, sr):
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_vals = pitches[magnitudes > np.median(magnitudes)]
    if len(pitch_vals) > 0:
        return np.mean(pitch_vals)
    return None

def main():
    print("Starting microphone stream... Press Ctrl+C to stop.")

    buffer_size = int(SAMPLE_RATE * CHUNK_DURATION)

    try:
        while True:
            # Record a short chunk
            audio_chunk = sd.rec(buffer_size, samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='float32')
            sd.wait()  # Wait for recording to finish
            y = audio_chunk.flatten()

            # Calculate volume and pitch
            volume = get_volume(y)
            pitch = get_pitch(y, SAMPLE_RATE)

            print(f"Volume: {volume:.2f} | Pitch: {pitch:.2f} Hz" if pitch else f"Volume: {volume:.2f} | Pitch: Unclear")

            # Sleep until next update (this is already synced by chunk duration)
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
