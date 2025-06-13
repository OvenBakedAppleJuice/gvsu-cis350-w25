import customtkinter as ctk
from GUI.ColorSelectFrame import ColorSelectFrame
# from main import AudioViz_GUI

class PlayPauseMode(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.parent = master
        self.configure(height=400, width=250)
        self.grid_propagate(False)

        self.menuSetup()

        self.color_hsv = None


    def playButtonClick(self):
        # If currently playing audio
        if self.parent._play_pause_pass:
            # action stops data pass and audio stream
            self.play.configure(fg_color="#20b502", text="Resume", hover_color="#167d01")
            self.parent._play_pause_pass = False
            self.parent.AudioControl.StopStream()
        # If not currently playing audio
        else:
            # action continues data pass and audio stream
            self.play.configure(fg_color="#db0909", text="Pause/Stop", hover_color="#a10303")
            self.parent._play_pause_pass = True
            self.parent.AudioControl.StartStream()

    def modeSelect(self):
        self.parent.switchArduinoAudioMode()
        if self.parent.ArduinoFreqMode:
            print("Freq Mode")
            self.modeButtonSelect.configure(text="Frequency\nMode")
        elif self.parent.ArduinoAmpMode:
            self.modeButtonSelect.configure(text="Amplitude\nMode")
            print("Amp Mode")



    #changes sens in main, adjusted on Amplitude multiplier
    def sliderEvent(self, value):
        self.parent.AudioControl.setSensativity(value)

    # grab color select hsv value
    def getHsvColor(self):
        return self.color_frame._hsv
    
    def getHexInt(self):
        return self.color_frame._intColor

    def menuSetup(self):
        #setup play button in frame
        self.play = ctk.CTkButton(self, text="Start", command=self.playButtonClick)
        self.play.grid(row=10, column=0, padx=20, pady=10)

        #Arduino Viz Mode Select
        self.modeButtonSelect = ctk.CTkButton(self, text="Amplitude\nMode", command=self.modeSelect, font=("Arial", 11))
        self.modeButtonSelect.grid(row=11, column=0, padx=20, pady=10)
        
        #setup slider for sensitivity
        self.sens_slider = ctk.CTkSlider(master=self, from_=0, to=10, number_of_steps=100, command=self.sliderEvent)
        self.sens_slider.set(1)
        self.sens_slider.grid(row=15, column=0, padx=20, pady=3)
        #label for sensitivity
        self.sens_label = ctk.CTkLabel(master=self, text=" Sensitivity: ", justify="left", compound="left", anchor="w")
        self.sens_label.grid(row=14, column=0, padx=20, pady=3, sticky="w")

        # add color picker, color picker sets by hex but returns hsv values
        self.color_frame = ColorSelectFrame(master=self, width=230, height=310)
        self.color_frame.grid(row=16, column=0, padx=1, pady=2)
            
    
        
        

        

# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("400x200")
#         self.grid_rowconfigure(0, weight=0)
#         self.grid_columnconfigure(0, weight=0)

#         self.my_frame = PlayPause(master=self, height=100)
#         self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# app = App()
# app.mainloop()