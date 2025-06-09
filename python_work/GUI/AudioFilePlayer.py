import customtkinter as ctk

class AudioFilePlayer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.parent = master

        self.active = False

        self.configure(height=220, width=500)
        self.grid_propagate(False)
        # file path stuff
        self._file_path = None
        self._file_name = None

        # audio file length
        self.start_time = 0.0  # start time in seconds, used for resuming playback

        self.menuSetup()
        
        # start disabled
        self.disabledAllWidgets()

    @property
    def file_name(self):
        return self._file_name
    
    @property
    def file_path(self):
        return self._file_path
    
    @file_path.setter
    def file_path(self, new_fp):
        self._file_name = (new_fp.split("/"))[-1]
        self._file_path = new_fp

    # Play/Pause Sound
    def playPauseSound(self):
        if self.file_path == None:
            return -1       #this shouldnt be possible
        if self.play_pause.cget("text") == "Pause":
            self.play_pause.configure(text="Resume", fg_color="#4888ff", hover_color="#3763C2")
            self.parent.AudioControl.PausePlayingAudioFile()
        elif self.play_pause.cget("text") == "Resume":
            self.play_pause.configure(text="Pause", fg_color="#a9c7ff", hover_color="#7287AA")
            # resume the music
            self.parent.AudioControl.ResumePlayingAudioFile()
        else:
            self.play_pause.configure(text="Pause", fg_color="#a9c7ff", hover_color="#7287AA")
            self.parent.AudioControl.StartPlayingAudioFile(self.file_path)

    # Restart Sound
    def restartSound(self):
        """
        Stops audio and resets to 0 seconds.
        """
        if self.file_path == None:
            return -1       #this shouldnt be possible
        self.parent.AudioControl.RestartPlayingAudioFile()
        self.play_pause.configure(text="Play", fg_color="#4888ff", hover_color="#3763C2")
        self.updateTimeDisplay()
        self.audio_timeline.set(0)


    # Volume Slider
    def volumeChange(self, volume: float):
        """
        Change volume of audio file, can happen in real time.
        """
        if self.file_path == None:
            return -1       #this shouldnt be possible
        volume = volume
        self.parent.AudioControl.setAudioFileVolume(volume)

    def updateTimeDisplay(self):
        if self.file_path is None:
            return -1
        else:    
            time = self.parent.AudioControl.getAudioFileTime()
            if time < 0.001:
                self.audio_timeline_cur_time.configure(text="--:--")
            else:
                self.audio_timeline_cur_time.configure(text=f"{int(time//60):02}:{int(time%60):02}")

    def updateTotalTime(self):
        if self.file_path is None:
            return -1
        else:    
            time = self.parent.AudioControl.getAudioFileTotalTime(self.file_path)
            if time < 0.001:
                self.audio_timeline_total_time.configure(text="--:--")
            else:
                self.audio_timeline_total_time.configure(text=f"Total Time {int(time//60):02}:{int(time%60):02}")
                self.audio_timeline.configure(from_=0, to=time, number_of_steps=200)

    def resetPlayer(self):
        """
        Resets file player widgets.
        """
        self.play_pause.configure(text="Play", fg_color="#4888ff", hover_color="#3763C2")
        self.disabledAllWidgets()
        self.enableAllWidgets()

    def startUpPlayerFromPath(self, file_path: str):
        # WILL NEED to implement method to stop current audio
        if not self.active:
            self.enableAllWidgets()
        else:
            self.resetPlayer()
        # auto sets file_name
        self.file_path = file_path
        self.file_name_label.configure(text=f"Using: {self.file_name}")
        self.updateTotalTime()


    def UpdateStartTime(self, startTime):
        """
        Stops the current program and moves to the spot in the file selected by the slider.
        """
        self.parent.AudioControl.EndPlayingAudioFile()
        self.parent.AudioControl.setStartTime(startTime)
        self.startUpPlayerFromPath(self.file_path)
        self.audio_timeline_cur_time.configure(text=f"{int(startTime//60):02}:{int(startTime%60):02}")


    def enableAllWidgets(self):
        self.active = True
        for widget in self.winfo_children():
            try:
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="#ffffff")
                else:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(state="normal")
            except Exception:
                pass    #some widgets like label dont have state

    def disabledAllWidgets(self):
        self.active = False
        for widget in self.winfo_children():
            try:
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="#828282")
                else:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(state="disabled")
            except Exception:
                pass    #some widgets like label dont have state

    def menuSetup(self): 
        # add items to frame
        
        # column 0
        self.frame_title = ctk.CTkLabel(master=self, text="MP3 File Player", font=("Roboto", 15))
        self.frame_title.grid(row=0, column=0, padx=5, pady=1)

        self.play_pause = ctk.CTkButton(master=self, text="Play", command=self.playPauseSound, hover_color="#476396", fg_color="#74a2f7", text_color="white")
        self.play_pause.grid(row=1, column=0, padx=5, pady=(1, 0))

        self.restart_btn = ctk.CTkButton(master=self, text="Restart", command=self.restartSound, hover_color="#5231B3", fg_color="#332995", text_color="white")
        self.restart_btn.grid(row=2, column=0, padx=5, pady=0)

        self.file_volume_label = ctk.CTkLabel(master=self, text="Volume", font=("Roboto", 15), width=200)
        self.file_volume_label.grid(row=3, column=0, padx=10, pady=0)
        self.file_volume= ctk.CTkSlider(master=self, from_=0, to=2, number_of_steps=200, command=self.volumeChange)
        self.file_volume.grid(row=4, column=0, padx=5, pady=0)
        self.file_volume.set(1)

        # column 1
        self.file_name_label = ctk.CTkLabel(master=self, text=f"Using: {self.file_name}", font=("Roboto", 15), width=200)
        self.file_name_label.grid(row=0, column=1, padx=5, pady=1)

        self.audio_timeline_cur_time = ctk.CTkLabel(master=self, text="--:--", font=("Roboto", 15), width=50, anchor="w", justify="left")
        self.audio_timeline_cur_time.grid(row=1, column=1, padx=10, pady=1, sticky="w")
        self.audio_timeline = ctk.CTkSlider(master=self, from_=0, to=1, number_of_steps=200, command=self.UpdateStartTime)
        self.audio_timeline.grid(row=2, column=1, padx=10, pady=20, sticky="ew")
        self.audio_timeline_total_time = ctk.CTkLabel(master=self, text="--:--", font=("Roboto", 15), width=50, anchor="e", justify="right")
        self.audio_timeline_total_time.grid(row=3, column=1, padx=10, pady=1, sticky="e")
        self.audio_timeline.set(0)

        self.widgets = [self.frame_title, self.play_pause, self.restart_btn, self.file_volume, self.file_name_label]

    