import customtkinter as ctk
# from main import AudioViz_GUI

class PlayPauseMode(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.parent = master

        #setup play button in frame
        self.play = ctk.CTkButton(self, text="Start", command=self.playButtonClick)
        self.play.grid(row=10, column=0, padx=20, pady=10)
        
        #setup slider for sensitivity
        self.sens_slider = ctk.CTkSlider(master=self, from_=50, to=200, number_of_steps=150, command=self.sliderEvent)
        self.sens_slider.set(100)
        self.sens_slider.grid(row=15, column=0, padx=20, pady=3)
        #label for sensitivity
        self.sens_label = ctk.CTkLabel(master=self, text=" Sensitivity: ", justify="left", compound="left", anchor="w")
        self.sens_label.grid(row=14, column=0, padx=20, pady=3, sticky="w")

    def playButtonClick(self):
        if self.play.cget("text") == "Pause/Stop":
            # action stops data pass
            self.play.configure(fg_color="#20b502", text="Resume", hover_color="#167d01")
            self.parent._play_pause_pass = False
        else:
            # action continues data pass
            self.play.configure(fg_color="#db0909", text="Pause/Stop", hover_color="#a10303")
            self.parent._play_pause_pass = True

    #changes sens in main, adjusted on Amplitude multiplier
    def sliderEvent(self, value):
        self.parent.sensitivity = value
            
    
        
        

        

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