import customtkinter as ctk
# from main import AudioViz_GUI

class PlayPauseMode(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        self.parent = master

        #setup play button in frame
        self.play = ctk.CTkButton(self, text="Start", command=self.playButtonClick)
        self.play.grid(row=10, column=0, padx=20, pady=10)


    def playButtonClick(self):
        if self.play.cget("text") == "Pause/Stop" or self.play.cget("text") == "Start":
            # action stops data pass
            self.play.configure(fg_color="#20b502", text="Resume", hover_color="#167d01")
            self.parent._play_pause_pass = False
        else:
            # action continues data pass
            self.play.configure(fg_color="#db0909", text="Pause/Stop", hover_color="#a10303")
            self.parent._play_pause_pass = True
            
        
        

        

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