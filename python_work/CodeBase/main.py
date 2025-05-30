from Audio import AudioInput
from Comms import USBComm 
from AudioVeiwer import PlotBins
from GUI.PlayPauseMode import PlayPauseMode

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

        # sensitivity variable (50 - 200) default 100. Might need changing
        # NOTE: sens doesnt work on the graph but for the arduino (i think)
        self.sensitivity = 50

        #allow passing of data (handled from PlayPauseMode Buttons)
        self._play_pause_pass = False

        #Set up application theme, color, and size
        self.geometry("950x550")
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

        self.ArduinoComms = USBComm()
        #print(self.ArduinoComms.getPortDesciptions())
        #print(self.ArduinoComms.getPorts())
        try:
            self.ArduinoComms.startComm('COM3')
        except Exception as e:
            print(e)

        #Aduio Veiwer
        self.binsPlot = PlotBins(self)

        #initializes and starts main task, daemon=True means the thread stops when the main thread stops
        #main_task = threading.Thread(target=self.mainLoop, daemon=True)
        #main_task.start()
        self.mainLoopUpdate = 1 #Sets the main loop to update every x ms
        self.after(self.mainLoopUpdate, self.mainLoop)
        self.maxAmplitude = 25000

    def mainLoop(self):
        """
        Main loop will handle comms to the arduino led visualization.
        """
        
        # if statement controled by PlayPauseMode buttons, contains handles to graph and Arduino
        #check if PlayPauseMode -> Play (Button) is enabled to continue loop
        if self._play_pause_pass:
            #data = self.AudioControl.GetAudioData()
            #data = self.AudioControl.GetAmplitude()
            #data = self.AudioControl.GetLargestMagFreq()
            data = self.AudioControl.GetSixteenFrequencies()
            #self.AudioControl.PrintSixteenBinsStr()
            plot = self.binsPlot.plotBins(data)
            plot.grid(row=0, column=20, rowspan=6, columnspan=7,
                        padx=0, pady=0, sticky=tk.NSEW)
            
            
            
            data = (self.AudioControl.GetAmplitude()/self.maxAmplitude)*self.sensitivity
            print(data)
            try:
                self.ArduinoComms.run(data)
            except Exception as e:
                None
        # Note: upon re-enabling, mainloop will be called
            
        # calls mainloop after 100ms
        self.after(self.mainLoopUpdate, self.mainLoop)        


    def menuSetup(self):
        """
        Creates the elements in the gui.
        """
        options = ["1","2","3"]
        self.dropdown = tk.CTkOptionMenu(self, values=options, command= (lambda x: self.dropdownCallback()))
        self.dropdown.grid(row=7, column=0, padx=0, pady=0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.play_pause = PlayPauseMode(master=self, height=400)
        self.play_pause.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

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
