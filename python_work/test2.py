import sounddevice as sd
import numpy as np
import soundfile as sf # For saving to WAV

DURATION = 5  # seconds
SAMPLE_RATE = 44100 # Hz
CHANNELS = 2 # Stereo

# --- Step 1: Find your loopback/stereo mix device ---
# Similar to PyAudio, you'll need to identify the correct input device.
# sd.query_devices() is useful for listing devices.
# Look for "Stereo Mix", "Loopback", or "Monitor of" devices.

print(sd.query_devices())
input_device_name = "Microsoft Sound Mapper" # Example for Windows, adjust for your OS/device
# input_device_name = "Loopback: PCM (hw:1,1)" # Example for Linux (adjust device number)
# input_device_name = "iShowU Audio Capture" # Example for macOS (if installed)

try:
    # Find the device index by name (or directly use an integer index if you know it)
    input_device_info = sd.query_devices(input_device_name, 'input')
    input_device_id = input_device_info['index']
except sd.PortAudioError:
    print(f"Error: Could not find input device named '{input_device_name}'.")
    print("Please check your audio device settings and available devices.")
    print("Try running 'python -c \"import sounddevice as sd; print(sd.query_devices())\"' to list devices.")
    exit()

print(f"* Recording from: {input_device_info['name']}")

try:
    # Record audio
    # The 'samplerate', 'channels', and 'dtype' should match your system audio settings
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE),
                        samplerate=SAMPLE_RATE,
                        channels=CHANNELS,
                        dtype='int16',
                        device=input_device_id)

    sd.wait() # Wait until recording is finished

    print("* Done recording.")

    # audio_data is already a NumPy array
    print(f"Shape of captured audio: {audio_data.shape}")

    # You can now process the audio_data (NumPy array)
    # For example, save to a WAV file:
    sf.write("system_audio_sd.wav", audio_data, SAMPLE_RATE)
    print("Saved to system_audio_sd.wav")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Ensure your loopback device is properly configured and selected.")
