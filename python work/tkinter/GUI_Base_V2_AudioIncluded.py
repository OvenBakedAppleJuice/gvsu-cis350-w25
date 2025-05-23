import customtkinter as tk


#import time
import numpy as np #For converting byte data into arrays

#for multithreading, and doing the audio IO while doing other stuff
import threading
import queue

import pyaudio
import sys
import time

class AudioInput:
    """
    This class is used for streaming and processing the audio.
    """
    def __init__(self):
        self.chunk = 2048  # Record in chunks of 1024 samples
        self.sampleFormat = pyaudio.paInt16  # 16 bits per sample (signed 16 bit)
        self.channels = 2
        self.fs = 48000  # Record at 48000 samples per second
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
        self.__stream = self.__port.open(format=self.sampleFormat,
                channels=self.channels,
                rate=self.fs,
                frames_per_buffer=self.chunk,
                input=True,
                input_device_index=self.__deviceIndex)

        #This loop runs abour every 42 ms (1/(48,000 samples/sec)*2048 samples)
        while True:
            #Check to see if steam is trying to be closed
            if not self.__stream_running:
                break

            try:
                #Reads "chunk" number of samples from microphone. They are read as bytes.
                sound_data = self.__stream.read(self.chunk) #blocking function, waits for 1024 samples

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

class Grid:
    def __init__(self, root, numRows, numCols):
        # Makes a fixed grid
        self.numRows = numRows
        self.numCols = numCols
        self.root = root
        self.setGrid()

    def setGrid(self):
        for i in range(self.numRows):
            self.root.rowconfigure(i, weight=1)
        for j in range(self.numCols):
            self.root.columnconfigure(j, weight=1)



class AudioViz_GUI(tk.CTk):
    """
    This is the outer program.
    """

    def __init__(self):
        super().__init__()

        #Set up application theme, color, and size
        self.geometry("750x550")
        self.minsize(width=750, height=550)
        self.title("Audio Visualizer")
        tk.set_default_color_theme("dark-blue")
        tk.set_widget_scaling(1.2)
        tk.set_appearance_mode("dark")

        #Set the program to close the application when the exit button is pressed
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        #Create a grid where menu items will be place
        self.grid = Grid(self, 18, 12)

        # Where the bulk of the menu buttons will be created.
        self.menuSetup()

        # Start the Audio Stream using the Audio Input Class
        self.AudioControl = AudioInput()
        self.AudioControl.ListDevicesStrings()
        self.AudioControl.StartStream()

        #initializes and starts main task
        main_task = threading.Thread(target=self.mainLoop)
        main_task.start()

    def mainLoop(self):
        while True:
            #data = self.AudioControl.GetAudioData()
            data = self.AudioControl.GetAmplitude()
            print(data)

            #Sleep for 1ms to reduce processing
            time.sleep(0.001)


    def menuSetup(self):
        options = ["1","2","3"]
        self.dropdown = tk.CTkOptionMenu(self, values=options, command= (lambda x: self.dropdownCallback()))
        self.dropdown.grid(row=2, column=3, padx=0, pady=0)

    def dropdownCallback(self):
        print("Here")

    def onClosing(self):
        """
        When the exit button is pressed.
        """
        self.AudioControl.StopStream()
        self.AudioControl.Terminate()

        self.destroy() #End tkinter application
        time.sleep(1)
        print("Program Complete.")
        sys.exit() #End program, closes all threads


#Initializes application
app = AudioViz_GUI()

#Starts application
app.mainloop()
