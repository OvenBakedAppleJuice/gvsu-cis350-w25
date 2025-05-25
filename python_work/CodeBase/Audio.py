import time
import numpy as np #For converting byte data into arrays
import pyaudio # For streaming audio in and out

#for multithreading, and doing the audio IO while doing other stuff
import threading
import queue


class AudioInput:
    """
    This class is used for streaming and processing the audio.
    """
    def __init__(self):
        self.__chunk = 2048  # Record in chunks of 1024 samples
        self.__sampleFormat = pyaudio.paInt16  # 16 bits per sample (signed 16 bit)
        self.__channels = 2
        self.__fs = 44100  # Record at 44100 samples per second
        self.__deviceIndex = 0 #This the device that audio will be stream to
        self.__port = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.__q = queue.Queue()
        #These are flags used to stop the audio stream
        self.__stream_running = False
        self.__stream_complete = True

    def SetDevice(self, device):
        """
        This is used to set an input device based on index.
        """
        devices = self.ListDevicesNumbers()

        if(device in devices):
            self.__deivceIndex = device
        else:
            print("Invalid Device.")

    def ListDevicesNumbers(self):
        """
        Returns a list of available deivce input index's.
        """
        info = self.__port.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        devices = []
        for i in range(0, numdevices):
            if (self.__port.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                devices.append(i)

        return devices

    def ListDevicesStrings(self):
        """
        Returns a list of strings describing available input devices.
        """
        #List all devices.
        info = self.__port.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        devices = []
        for i in range(0, numdevices):
            if (self.__port.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                string = "Input Device id ", i, " - ", self.__port.get_device_info_by_host_api_device_index(0, i).get('name')
                print(string)
                devices.append(string)

            #if (self.__port.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                # Print out output devices, don't return them as they can't be used.
                #print("Output Device id ", i, " - ", self.__port.get_device_info_by_host_api_device_index(0, i).get('name'))

        return devices

    def StartStream(self):
        print("#" * 80)
        print("#" * 80)

        #initializes and starts task
        self.playing_task = threading.Thread(target=self.RunStream)
        self.__stream_running = True
        self.__stream_complete = False
        self.playing_task.start()

        print('-----Now Streaming-----')

    def RunStream(self):
        """
        Defines a task that will get the audio at regular interval.
        """
        self.__stream = self.__port.open(format=self.__sampleFormat,
                channels=self.__channels,
                rate=self.__fs,
                frames_per_buffer=self.__chunk,
                input=True,
                input_device_index=self.__deviceIndex)

        #This loop runs abour every 42 ms (1/(48,000 samples/sec)*2048 samples)
        while True:
            #Check to see if steam is trying to be closed
            if not self.__stream_running:
                break

            try:
                #Reads "chunk" number of samples from microphone. They are read as bytes.
                sound_data = self.__stream.read(self.__chunk) #blocking function, waits for 1024 samples

                #puts the sound data to the queue so it can be accessed elsewhere
                self.__q.put(sound_data)

            except Exception as e:
                print("LiveView: playing_task, audio_frame_queue is empty.")
                continue

        #Stream has been closed
        self.__stream_complete = True

    def StopStream(self):
        """
        Stop Stream. Another stream could be started.
        """
        self.__stream_running = False
        print("Stopping Steam...")
        #Wait for stream to close
        while(not self.__stream_complete):
            time.sleep(0.001)

        self.__stream.close()
        print("Stream stopped.")

    def GetAudioData(self):
        """
        Returns an array with 1024 int16 data values. This is the most recent audio chunk.
        """
        # gets command from queue
        sound = self.__q.get() #currently in 'bytes' format

        #Clears queue if it was not accessed quickly enough
        while(not self.__q.empty()):
            self.__q.get()

        # Convert bytes to
        audio_int16_array = np.frombuffer(sound, dtype=np.int16).view(dtype=np.int16)
        #Collecting the max value just to show the data.
        return audio_int16_array


    def GetAmplitude(self):
        """
        Returns an array with 1024 int16 data values. This is the most recent audio chunk.
        """
        # gets command from queue
        sound = self.__q.get() #currently in 'bytes' format

        #Clears queue if it was not accessed quickly enough
        while(not self.__q.empty()):
            self.__q.get()

        # Convert bytes to
        audio_int16_array = np.frombuffer(sound, dtype=np.int16).view(dtype=np.int16)

        maxVal = audio_int16_array.max()
        minVal = audio_int16_array.min()

        #Collecting the max value just to show the data.
        return maxVal-minVal

    def Terminate(self):
        """
        Terminate port at end of program.
        """
        self.__port.terminate()