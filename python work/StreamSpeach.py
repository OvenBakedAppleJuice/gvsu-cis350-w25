#This demonstrates pyaudio as a way to get microphone data.

#///////////////////////Libraries/////////////////////////////////
#for other purposes
# For streaming the computer system audio a library the stereo mix may need to be enabled:
# https://shankhanilborthakur.medium.com/recording-system-audio-in-windows-10-using-pyaudio-1559f3e1b64f

import time
import numpy as np #For converting byte data into arrays

#for multithreading, and doign the audio IO while doing other stuff
import threading
import queue

import pyaudio

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample (signed 16 bit)
channels = 2
fs = 48000  # Record at 48000 samples per second



#////////////////////////////////Main/////////////////////////////////////////////
def main():
    print("#" * 80)
    print("#" * 80)

    #initializes and starts task
    playing_task = threading.Thread(target=receive_sound__task)
    playing_task.start()

    print('-----Now Recording-----')
    first = True
    #Looped Section of Code/////////////////////////////////////////////////////////////////
    while True:
        # gets command from queue
        sound = q.get() #currently in 'bytes' format

        #Clears queue if it was not accessed quickly enough
        while(not q.empty()):
            q.get()

        # Convert bytes to
        int16_array = np.frombuffer(sound, dtype=np.int16).view(dtype=np.int16)
        #Collecting the max value just to show the data.
        print(int16_array.max())


def receive_sound__task():
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    #List all devices.
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


    stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True,
                input_device_index=1)

    #optionally can add, input_device_index=0,1,2,tc. to above. This selects the audio.



    while True:
        try:
            #Reads "chunk" number of samples from microphone. They are read as bytes.
            sound_data = stream.read(chunk)

            #puts the sound data to the queue so it can be accessed in the main loop.
            q.put(sound_data)

        except Exception as e:
            print("LiveView: playing_task, audio_frame_queue is empty.")
            continue

        """
        # This version works similar to above, but collects multiple frames at once. Each frame has "chunk" number of samples.
        frames = []
        #You can change the number of frames.
        for i in range(0, numFrames):
            try:
                frame = stream.read(chunk)
                frames.append(frame)

                #b''.join(frames) combines the frames together
                #sound_data = b''.join(frames)

                #puts the sound data to the queue so it can be accessed in the main loop
                q.put(sound_data)

            except Exception as e:
                print("LiveView: playing_task, audio_frame_queue is empty.")
                continue
        """


#///////////////CODE START/////////////////////////
if __name__ == '__main__':

    #opens queue that command will be written to
    q = queue.Queue()

    main()
