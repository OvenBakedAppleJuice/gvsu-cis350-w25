import time
import numpy as np #For converting byte data into arrays
import pyaudio # For streaming audio in and out
from pydub import AudioSegment

#for multithreading, and doing the audio IO while doing other stuff
import threading
import queue
import os

class AudioInput:
    """
    This class is used for streaming and processing the audio.
    """
    def __init__(self):
        # Used by pydub to convert mp3 files to wave files
        AudioSegment.converter = 'ffmpeg.exe'
        AudioSegment.ffprobe = 'ffprobe.exe'

        #Used by pyaudio to stream audio
        self.__chunk = 2048  # Record in chunks of 1024 samples
        self.__sampleFormat = pyaudio.paInt16  # 16 bits per sample (signed 16 bit)
        self.__channels = 2
        self.__default_fs = 44100
        self.__fs = 44100  # fs: frequency of sample. Record at 44100 samples per second
        self.__deviceIndex = 0 #This the device that audio will be stream to
        self.__port = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.__stream = None
        self.__q = queue.Queue()
        
        #These are variables used to stop the audio input stream
        self.__input_stream_running = False
        self.__input_stream_complete = True

        #These are variables used for controlling an audio file output stream
        self.__output_stream_running = False
        self.__output_stream_pause = False
        self.__output_stream_complete = True
        self.__audio_data_chunks = []
        self.__num_audio_file_chunks = 0
        self.__audio_file_cur_time = 0
        self.__audio_file_start_time = 0
        self.__volume = 1

        #These are variables that relate to getting sixteen frequency magnitude or one amplitude magnitude
        self.__audio_int16_array = None
        self.__sensativity_multiplier = 1
        self.__max_amplitude = 65536
        
        #Setup up for fft
        # sample spacing
        T = 1.0 / self.__fs
        #X time axis for one audio chunk (lowest detectable freq will be 25 Hz)
        self.__fft_x = np.linspace(0.0, self.__chunk*T, self.__chunk, endpoint=False)
    
    # REGION Set and Get Input Audio Devices ******************************************************
    def SetDevice(self, device):
        """
        This is used to set an input device based on index.
        """
        self.__deivceIndex = device

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
                string = "Input ID "+ str(i)+ "-" + self.__port.get_device_info_by_host_api_device_index(0, i).get('name')
                print(string)
                devices.append(string)

            #if (self.__port.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                # Print out output devices, don't return them as they can't be used.
                #print("Output Device id ", i, " - ", self.__port.get_device_info_by_host_api_device_index(0, i).get('name'))

        return devices

    def getDefaultDevice(self):
        return self.__port.get_default_input_device_info().get('index')

    # REGION Getting FFT and Amplitude ******************************************************
    def setSensativity(self, multiplier):
        if(0 <= multiplier <= 1000):
            self.__sensativity_multiplier = multiplier
    
    def setMaxAmplitude(self, maxAmplidute):
        if(1 <= maxAmplidute <= 1000000):
            self.__max_amplitude = maxAmplidute

    def getMaxAmplitude(self):
        return self.__max_amplitude
    
    def getSensativity(self):
        return self.__sensativity_multiplier

    def GetSixteenFrequencies(self):
        freq, mags = self.__getFft()
        freqBins = [(0, 100), (100, 160), (160, 220), (220, 280), (280, 340), (340, 400), (400, 460), 
                    (460, 520), (520, 580), (580, 640), (640, 700), (700, 760), (760, 820), 
                    (820, 880), (880, 940), (1000, 20000)]
        
        binIndicies = [[] for i in range(16)]
        binMagnitudes = [0 for i in range(16)]

        # Loop through the indicies
        for i, bin in enumerate(freqBins):
            # Get the frequencies in the range of the bin
            freqInRange = ((bin[0]<=freq) & (freq<bin[1]))
            # Get the indicies of those frequencies
            binIndicies[i] = np.where(freqInRange)
            # Get the magnitude of values in a bin
            binMagnitudes[i] = mags[binIndicies[i]]
            
            #This gets the average value of a bin
            binMagnitudes[i] = int(np.mean(binMagnitudes[i])*self.__sensativity_multiplier)

            # This version gets the max
            # binMagnitudes[i] = int(max(binMagnitudes[i]))
        
        return binMagnitudes

    def GetAmplitude(self):
        """
        Returns an array with 1024 int16 data values. This is the most recent audio chunk.
        """
        maxVal = self.__audio_int16_array.max()
        minVal = self.__audio_int16_array.min()

        #Collecting the max value just to show the data.
        return abs(round((maxVal-minVal)/self.__max_amplitude*100*self.__sensativity_multiplier))

    def __getFft(self):
        """
        Sources: 
        https://docs.scipy.org/doc/scipy/tutorial/fft.html
        https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter24.04-FFT-in-Python.html
        """
        signal = self.GetAudioData()
        # signal = signal / np.max(np.abs(signal))

        # Apply the FFT. The output is complex.
        fft_output = np.fft.fft(signal)

        # The magnitude of each complex number in the FFT output.
        magnitudes = np.abs(fft_output)

        # The frequencies array will have the same length as the fft_output.
        # numpy.fft.fftfreq helps in generating the correct frequency bins.
        frequencies = np.fft.fftfreq(self.__chunk, d=1/self.__fs)

        # For a real-valued input signal, the FFT output is symmetric.
        # We only need the first half (positive frequencies).
        # The index N/2 + 1 typically includes the DC component (0 Hz) and the Nyquist frequency.
        num_unique_points = self.__chunk // 2 + 1 # For even N, this is N/2 + 1. For odd N, this is (N+1)/2

        frequencies_positive = frequencies[0:num_unique_points]
        magnitudes_positive = magnitudes[0:num_unique_points]

        return frequencies_positive, magnitudes_positive

    def GetLargestMagFreq(self):
        """
        Returns the frequency with the largest magnitude.
        """
        freq, mags = self.__getFft()
        largest = mags.argmax()
        
        return freq[largest]

    def PrintSixteenBinsStr(self):
        """
        Prints out the bins in a readable form.
        """
        data = self.GetSixteenFrequencies()
        for number in data:
            print(f" {number:7}", end="")
        print() # Add a newline at the end

    # REGION general ****************************************************************
    def Terminate(self):
        """
        Terminate port at end of program.
        """
        self.__port.terminate()

    # REGION playing MP3 files ******************************************************
    def setStartTime(self, startTime):
        """
        Sets start time for audio file.
        """
        if 0 < startTime < 100000:
            self.__audio_file_start_time = startTime
            
    def ConvertMP3File(self, mp3_filepath):
        """
        Converts mp3 file to wave format and updates self.__audio_data_chunks along with 
        a few other important variables for audio oputput.
        """
        print(mp3_filepath)
        if not os.path.exists(mp3_filepath):
            print(f"Error: MP3 file not found at '{mp3_filepath}'")
            return

        try:
            print(f"Loading '{mp3_filepath}' for playback...")
            audio = AudioSegment.from_mp3(mp3_filepath)

            # PyAudio parameters
            self.__fs = audio.frame_rate

            # Convert pydub audio to raw PCM data
            raw_audio_data = audio.raw_data

            # Split raw_audio_data into chunks for the callback
            # Each chunk should be `chunk_size` frames.
            # A frame consists of (CHANNELS * (FORMAT_BYTES_PER_SAMPLE)) bytes.
            bytes_per_frame = self.__channels * pyaudio.get_sample_size(self.__sampleFormat)
            bytes_per_chunk = self.__chunk * bytes_per_frame

            self.__audio_data_chunks = []
            for i in range(0, len(raw_audio_data), bytes_per_chunk):
                self.__audio_data_chunks.append(raw_audio_data[i:i + bytes_per_chunk])
            self.__num_audio_file_chunks = len(self.__audio_data_chunks)
        
        except Exception as e:
            print("Conversion Error")
            print(e)

    def StartPlayingAudioFile(self, file):
        """
        Starts the audio output stream of an MP3 file.
        """
        self.__audio_file_cur_time = 0
        self.ConvertMP3File(file)
        self.__output_stream_running = True
        self.playing_task = threading.Thread(target=self.RunAudioFileStream)
        self.playing_task.start()

    
    def RunAudioFileStream(self):
        """
        Runs in a seprate thread and plays output audio data.
        """
        self.__stream = self.__port.open(format=self.__sampleFormat,
                channels=self.__channels,
                rate=self.__fs,
                frames_per_buffer=self.__chunk,
                output=True,)

        self.__start_audio_chunk = (self.__audio_file_start_time * self.__fs)/self.__chunk

        # Play the audio in chunks
        for i in range(self.__num_audio_file_chunks):
            chunk =  self.__audio_data_chunks[i]

            if i < self.__start_audio_chunk:
                continue

            self.__audio_file_cur_time = (i * self.__chunk) / self.__fs
            

            if not self.__output_stream_running:
                break
            
            #if paused wait to be unpaused or stopped
            if self.__output_stream_pause:
                wasClosed = False
                while(self.__output_stream_pause):
                    time.sleep(0.01) #slight delay to prevent too much processing
                    if(not self.__output_stream_running):
                        asClosed = True
                        break   
                if wasClosed:
                    break
            
            try:
                chunk = np.frombuffer(chunk, np.int16) #parse bytes into numpy array
                chunk = chunk * self.__volume #scale chunk by volume
                chunk = np.clip(chunk, -32768, 32767) # avoid oveflow
                chunk = chunk.astype(np.int16) #convert back to int16
                self.__q.put(chunk)
                chunk = chunk.tobytes() #convert back to bytes for stream
                #blocks while streaming
                self.__stream.write(chunk) #convert numpy array back to bytes and stream data 
            except Exception as e:
                print(e)
                break
        
        self.__output_stream_running = False
        self.__output_stream_pause = False
        self.__stream.close()
    
    def getAudioStreamRunning(self):
        """
        Returns a bool if the audio stream thread is running.
        """
        return self.__output_stream_running and (not self.__output_stream_pause)

    def getAudioFileTotalTime(self, path):
        """
        Gets the total time length of an MP3 file.
        """
        try:
            audio = AudioSegment.from_mp3(path)

            # Duration in seconds (float)
            return audio.duration_seconds
        except Exception as e:
            print(e)
            return 0

    def getAudioFileTime(self):
        """
        Gets the current time of the audio file.
        """
        return self.__audio_file_cur_time

    def PausePlayingAudioFile(self):
        """
        Pauses audio output stream.
        """
        self.__output_stream_pause = True
    
    def ResumePlayingAudioFile(self):
        """
        Resumes audio output stream.
        """
        self.__output_stream_pause = False
    
    def RestartPlayingAudioFile(self):
        """
        Ends audio output stream and restarts it.
        """
        self.EndPlayingAudioFile()
        self.__audio_file_cur_time = 0
        self.__audio_file_start_time = 0

    def EndPlayingAudioFile(self):
        """
        Stops audio output and waits for thread to finish.
        """
        self.__output_stream_running = False
        if not (self.playing_task is None):
            if self.playing_task.is_alive():
                self.playing_task.join()
        self.__audio_file_cur_time = 0

    def setAudioFileVolume(self, volume):
        """
        Sets the volume of the output file.
        """
        if 0 < volume < 10:
            self.__volume = volume

    # REGION Start and run Input Audio Stream ******************************************************
    def StartStream(self):
        print("#" * 80)
        print("#" * 80)
        self.__fs = self.__default_fs
        #initializes and starts task
        self.playing_task = threading.Thread(target=self.RunStream)
        self.__input_stream_running = True
        self.__input_stream_complete = False
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
            if not self.__input_stream_running:
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
        self.__input_stream_complete = True

    def StopStream(self):
        """
        Stop Stream. Another stream could be started.
        """
        self.__input_stream_running = False
        print("Stopping Steam...")
        #Wait for stream to close
        while(not self.__input_stream_complete):
            time.sleep(0.001)
        
        if self.__stream is not None:
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
        self.__audio_int16_array = np.frombuffer(sound, dtype=np.int16).view(dtype=np.int16)
        #Collecting the max value just to show the data.
        return self.__audio_int16_array


# def freqBins():
#     """
#     Used to generate the bins in GetSixteenFrequencies() function. Helper function for making code.
#     """
#     i = 0
#     vals = []
#     maxEver = 20000
#     maxVal = 2000
#     iterVal = int(maxVal/15)

#     for j in range(15):
#         vals.append((i, i+iterVal))
#         i+=iterVal

#     vals.append((i, maxEver))

#     print(vals)