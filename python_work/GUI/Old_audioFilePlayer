import customtkinter as ctk
from mutagen.mp3 import MP3
import pygame
import time

class AudioFilePlayer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.active = False

        self.configure(height=220, width=500)
        self.grid_propagate(False)
        # file path stuff
        self._file_path = None
        self._file_name = None

        # audio file length
        self.audio_length = 0.0  # in seconds, will be set when file is loaded
        self.audio_length_str = '-:--'
        self.time_passed = 0.0  # time passed in seconds, will be set when file is loaded
        self.time_passed_str = '0:00' 
        self.audio_playing = False
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
            pygame.mixer.music.pause()
            self.audio_playing = False
        elif self.play_pause.cget("text") == "Resume":
            self.play_pause.configure(text="Pause", fg_color="#a9c7ff", hover_color="#7287AA")
            # resume the music
            pygame.mixer.music.unpause()
            self.audio_playing = True
            self.updateTime()  # continue updating the time display
        else:
            self.play_pause.configure(text="Pause", fg_color="#a9c7ff", hover_color="#7287AA")
            # playsound will block the thread, so this is not ideal for a GUI
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()
            self.audio_playing = True
            self.updateTime()  # start updating the time display

    # Restart Sound

    def restartSound(self):
        if self.file_path == None:
            return -1       #this shouldnt be possible
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.file_path)
        self.play_pause.configure(text="Play", fg_color="#4888ff", hover_color="#3763C2")
        self.audio_playing = False
        self.setupTimeLine()  # reset the timeline

    # Volume Slider

    def volumeChange(self, volume: float):
        if self.file_path == None:
            return -1       #this shouldnt be possible
        volume = volume / 100  # convert to 0-1 range
        pygame.mixer.music.set_volume(volume)

    # Audio Time Slider

    def audioTimeChange(self, time_set: float):
        # pygame.mixer.music.load(self.file_path)
        print(f"Setting time to: {time_set} seconds")
        self.start_time = time_set
        pygame.mixer.music.play(start=time_set)
        self.time_passed = time_set
        self.updateTimeDisplay()  # update the display immediately
    
    def updateTime(self):
        print(self.audio_playing)
        if self.audio_playing:
            self.time_passed = (pygame.mixer.music.get_pos() / 1000) + self.start_time
            print(f"Time passed: {self.time_passed} seconds")
            self.after(1000, self.updateTime)  # update every second
            self.updateTimeDisplay()


    def updateTimeDisplay(self):
        if self.file_path is None:
            return -1
        self.time_passed_str = time.strftime('%M:%S', time.gmtime(self.time_passed))
        self.audio_timeline_cur_time.configure(text=self.time_passed_str)
        self.audio_timeline.set(self.time_passed)

    def setupTimeLine(self):
        self.time_passed = 0.0
        self.time_passed_str = '0:00'
        self.audio_timeline_cur_time.configure(text=self.time_passed_str)
        self.audio_length = MP3(self.file_path).info.length
        self.audio_length_str = time.strftime('%M:%S', time.gmtime(self.audio_length))
        self.audio_timeline_total_time.configure(text=self.audio_length_str)
        self.audio_timeline.set(0)
        self.audio_timeline.configure(from_=0, to=self.audio_length, number_of_steps=self.audio_length)
        self.start_time = 0.0  # reset start time for new audio file

    # frame startup, enabling, and disabling
            
    def resetPlayer(self):
        self.play_pause.configure(text="Play", fg_color="#4888ff", hover_color="#3763C2")
        self.disabledAllWidgets()
        self.enableAllWidgets()

    def startUpPlayerFromPath(self, file_path: str):
        # WILL NEED to implement method to stop current audio
        self.audio_playing = False
        if not self.active:
            self.enableAllWidgets()
        else:
            self.resetPlayer()
        # auto sets file_name
        self.file_path = file_path
        self.file_name_label.configure(text=f"Using: {self.file_name}")
        # setup timeline
        self.setupTimeLine()

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
        self.audio_playing = False
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
        self.file_volume= ctk.CTkSlider(master=self, from_=0, to=100, number_of_steps=100, command=self.volumeChange)
        self.file_volume.grid(row=4, column=0, padx=5, pady=0)

        # column 1
        self.file_name_label = ctk.CTkLabel(master=self, text=f"Using: {self.file_name}", font=("Roboto", 15), width=200)
        self.file_name_label.grid(row=0, column=1, padx=5, pady=1)

        self.audio_timeline_cur_time = ctk.CTkLabel(master=self, text="0:00", font=("Roboto", 15), width=50, anchor="w", justify="left")
        self.audio_timeline_cur_time.grid(row=1, column=1, padx=10, pady=1, sticky="w")
        self.audio_timeline = ctk.CTkSlider(master=self, from_=0, to=1, number_of_steps=1, command=self.audioTimeChange)
        self.audio_timeline.grid(row=2, column=1, padx=10, pady=20, sticky="ew")
        self.audio_timeline_total_time = ctk.CTkLabel(master=self, text=self.audio_length_str, font=("Roboto", 15), width=50, anchor="e", justify="right")
        self.audio_timeline_total_time.grid(row=3, column=1, padx=10, pady=1, sticky="e")
        self.audio_timeline.set(1)

        # self.widgets = [self.frame_title, self.play_pause, self.restart_btn, self.file_volume, self.file_name_label, self.]

    