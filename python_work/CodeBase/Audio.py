import time
import numpy as np #For converting byte data into arrays
import sounddevice as sd # For streaming audio in and out

#for multithreading, and doing the audio IO while doing other stuff
import threading
import queue


class AudioInput:
    """
    This class is used for streaming and processing the audio.
    """
    def __init__(self):
        self.__chunk = 2048  # Record in chunks of 1024 samples
        self.__sampleFormat = 'int16' # 16 bits per sample (signed 16 bit)
        self.__channels = 2
        self.__fs = 44100  # fs: frequency of sample. Record at 44100 samples per second
        self.__deviceIndex = 0 #This the device that audio will be stream to
        self.__q = queue.Queue()
        #These are flags used to stop the audio stream
        self.__stream_running = False
        self.__stream_complete = True

        self.audio_int16_array = None

        #Setup up for fft
        # sample spacing
        T = 1.0 / self.__fs
        #X time axis for one audio chunk (lowest detectable freq will be 25 Hz)
        self.__fft_x = np.linspace(0.0, self.__chunk*T, self.__chunk, endpoint=False)

    def setIndex(self, index):
        self.__deviceIndex = index

    def getFft(self):
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
        freq, mags = self.getFft()
        largest = mags.argmax()
        
        return freq[largest]
    
    def GetSixteenFrequencies(self):
        freq, mags = self.getFft()
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
            binMagnitudes[i] = int(np.mean(binMagnitudes[i]))

            # This version gets the max
            # binMagnitudes[i] = int(max(binMagnitudes[i]))
        
        return binMagnitudes

    def PrintSixteenBinsStr(self):
        """
        Prints out the bins in a readable form.
        """
        data = self.GetSixteenFrequencies()
        for number in data:
            print(f" {number:7}", end="")
        print() # Add a newline at the end


    def SetDevice(self, device):
        """
        This is used to set an input device based on index.
        """
        devices = self.ListDevicesNumbers()

        if(device in devices):
            self.__deviceIndex = device
        else:
            print("Invalid Device.")

    def ListDevicesNumbers(self):
        """
        Lists all available sound input devices using sounddevice.
        """
        print("Available Input Devices:")
        devices = []
        try:
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    device = f"  {i}: {device['name']} (Channels: {device['max_input_channels']})"
                    devices.append(device)
                    print(device)
        except Exception as e:
            print(f"Error querying devices: {e}")
        
        deviceNumbers = []
        for i in range(len(devices)):
            deviceNumbers.append(i)
        return deviceNumbers

    def ListDevicesStrings(self):
        """
        Lists all available sound input devices using sounddevice.
        """
        print("Available Input Devices:")
        devices = []
        try:
            devices = sd.query_devices()
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    device = f"  {i}: {device['name']} (Channels: {device['max_input_channels']})"
                    devices.append(device)
                    print(device)
        except Exception as e:
            print(f"Error querying devices: {e}")
        
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
        with sd.InputStream(samplerate=44100, channels=1, dtype=self.__sampleFormat, device=self.__deviceIndex) as self.__stream:

            #This loop runs abour every 42 ms (1/(48,000 samples/sec)*2048 samples)
            while True:
                #Check to see if steam is trying to be closed
                if not self.__stream_running:
                    break

                try:
                    #Reads "chunk" number of samples from microphone. They are read as bytes.
                    sound_data, overflow = self.__stream.read(self.__chunk) #blocking function, waits for 1024 samples

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
        self.audio_int16_array = sound # np.frombuffer(sound, dtype=np.int16).view(dtype=np.int16)
        
        #Collecting the max value just to show the data.
        return sound


    def GetAmplitude(self):
        """
        Returns an array with 1024 int16 data values. This is the most recent audio chunk.
        """
        # gets command from queue
        #sound = self.__q.get() #currently in 'bytes' format

        #Clears queue if it was not accessed quickly enough
        #while(not self.__q.empty()):
        #    self.__q.get()

        # Convert bytes to
        #self.audio_int16_array = np.frombuffer(sound, dtype=np.int16).view(dtype=np.int16)

        maxVal = self.audio_int16_array.max()
        minVal = self.audio_int16_array.min()

        #Collecting the max value just to show the data.
        return maxVal-minVal

    def Terminate(self):
        """
        Terminate port at end of program.
        """
        self.__port.terminate()

def freqBins():
    """
    Used to generate the bins in GetSixteenFrequencies() function.
    """
    i = 0
    vals = []
    maxEver = 20000
    maxVal = 2000
    iterVal = int(maxVal/15)

    for j in range(15):
        vals.append((i, i+iterVal))
        i+=iterVal

    vals.append((i, maxEver))

    print(vals)