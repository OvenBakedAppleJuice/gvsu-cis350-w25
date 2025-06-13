from Audio import AudioInput
from Comms import USBComm 
from AudioVeiwer import PlotBins
from GUI.PlayPauseMode import PlayPauseMode
from GUI.SourceTab import SourcesTab
from GUI.AudioFilePlayer import AudioFilePlayer

import customtkinter as tk

import sys
import time 


class Grid:
    """
    Makes a simple fixed grid that elements can be added to.
    """
    def __init__(self, root, numRows, numCols):
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
    This class is the gui and has all the logic for controlling the audio stream and comms.
    """

    def __init__(self):
        super().__init__()

        #allow passing of data (handled from PlayPauseMode Buttons)
        self._play_pause_pass = False

        #Set up application theme, color, and size
        self.geometry("1050x600")
        self.minsize(width=750, height=550)
        self.title("Audio Visualizer")
        tk.set_default_color_theme("dark-blue")
        # tk.set_widget_scaling(1)
        tk.set_appearance_mode("dark")

        #Set the program to close the application when the exit button is pressed
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        #Create a grid where menu items will be place
        self.grid = Grid(self, 18, 12)


        # Start the Audio Stream using the Audio Input Class
        self.AudioControl = AudioInput()

        self.ArduinoControl = USBComm()
        self.ArduinoAmpMode = True
        self.ArduinoFreqMode = False

        #Aduio Veiwer
        self.binsPlot = PlotBins(self)
        
        # Where the bulk of the menu buttons will be created.
        self.menuSetup()

        #Runs the main loop
        self.mainLoopUpdate = 20 #Sets the main loop to update every x ms
        self.after(self.mainLoopUpdate, self.mainLoop)

    def switchArduinoAudioMode(self):
        """
        Switches between two arduino display modes
        """
        if self.ArduinoAmpMode:
            self.ArduinoAmpMode=False
            self.ArduinoFreqMode=True
        else:
            self.ArduinoAmpMode=True
            self.ArduinoFreqMode=False
    
    def mainLoop(self):
        """
        Main loop will handle comms to the arduino led visualization. Different from mainloop() 
        which is an internal function that calls the GUI display functions and handles the callbacks.
        """
        AudioFileIsRunning = self.AudioControl.getAudioStreamRunning()
        if AudioFileIsRunning:
            self.audio_file_player.updateTimeDisplay()
        
        color = self.play_pause.getHexInt()
        # print(color)
        hsv_color = self.play_pause.getHsvColor()[0]
        print(hsv_color)

        # if statement controled by PlayPauseMode buttons, contains handles to graph and Arduino
        #check if PlayPauseMode -> Play (Button) is enabled to continue loop
        if self._play_pause_pass or AudioFileIsRunning:
            data = self.AudioControl.GetSixteenFrequencies()
                
            plot = self.binsPlot.plotBins(data)
            plot.grid(row=0, column=2, padx=0, pady=0)
                
            if self.ArduinoAmpMode:
                color = str(self.play_pause.getHsvColor())
                amplitude = str(self.AudioControl.GetAmplitude())
                data = color + "," + amplitude
                print(f"Data is {data}")

            if self.ArduinoFreqMode:
                color = str(self.play_pause.getHsvColor())
                data = self.AudioControl.GetSixteenFrequencies()
                # Get min and max values
                min_val = 0
                max_val = 500000
                # Scale to integers from 0 to 16
                scaled = [round((x - min_val) / (max_val - min_val) * 16) for x in data]
                # Create comma-separated string
                formatted_result =  ",".join(str(x) for x in scaled)

                data = color + "," + formatted_result

            if self.ArduinoControl.isConnected():
                try:
                    self.ArduinoControl.run(data)
                except Exception as e:
                    None
            
        # calls mainloop after 100ms
        self.after(self.mainLoopUpdate, self.mainLoop)        

    def menuSetup(self):
        """
        Creates the elements in the gui.
        """
        self.play_pause = PlayPauseMode(master=self, height=400)
        self.play_pause.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")

        # setup for AudioSource Tabs
        self.audio_source_tab = SourcesTab(master=self)
        self.audio_source_tab.grid(row=4, column=0, padx=20, pady=5)

        #setup for AudioFilePlayer
        self.audio_file_player = AudioFilePlayer(master=self)
        self.audio_file_player.grid(row=4, column=2, padx=0, pady=20)

        # setup for base chart (no data)
        plot = self.binsPlot.plotBinsEmpty()
        plot.grid(row=0, column=2, padx=0, pady=0)
        
    def dropdownCallback(self):
        print("Here")

    def onClosing(self):
        """
        When the exit button is pressed.
        """
        try:
            self.AudioControl.EndPlayingAudioFile()
            self.AudioControl.StopStream()
            self.AudioControl.Terminate()

            self.destroy() #End tkinter application
            time.sleep(1)
            print("Program Complete.")
        except Exception as e:
            print(e)
        sys.exit() #End program, closes all threads


#Initializes application
app = AudioViz_GUI()

#Starts application
app.mainloop()
