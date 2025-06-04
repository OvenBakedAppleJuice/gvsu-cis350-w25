import customtkinter as ctk
import pyaudio
import pygame

class AudioFilePlayer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.active = False

        self.configure(height=200, width=600)

        self._file_path = None
        self._file_name = None

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

    def playPauseSound(self):
        if self.file_path == None:
            return -1       #this shouldnt be possible
        if self.play_pause.cget("text") == "Pause":
            self.play_pause.configure(text="Resume", fg_color="#4888ff", hover_color="#3763C2")
            pygame.mixer.music.pause()
        elif self.play_pause.cget("text") == "Resume":
            self.play_pause.configure(text="Pause", fg_color="#a9c7ff", hover_color="#7287AA")
            # resume the music
            pygame.mixer.music.unpause()
        else:
            self.play_pause.configure(text="Pause", fg_color="#a9c7ff", hover_color="#7287AA")
            # playsound will block the thread, so this is not ideal for a GUI
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()




    def startUpPlayerFromPath(self, file_path: str):
        # WILL NEED to implement method to stop current audio
        if not self.active:
            self.enableAllWidgets()
        else:
            self.resetPlayer()
        # auto sets file_name
        self.file_path = file_path
        self.file_name_label.configure(text=f"Using: {self.file_name}")

    def resetPlayer(self):
        self.play_pause.configure(text="Play", fg_color="#4888ff", hover_color="#3763C2")
        self.disabledAllWidgets()
        self.enableAllWidgets()


    def enableAllWidgets(self):
        self.active = True
        for widget in self.widgets:
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
        for widget in self.widgets:
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
        # NOTE ensure items are added to list
        self.frame_title = ctk.CTkLabel(master=self, text="MP3 File Player", font=("Roboto", 15))
        self.frame_title.grid(row=0, column=0, padx=5, pady=5)

        self.play_pause = ctk.CTkButton(master=self, text="Play", command=self.playPauseSound, hover_color="#476396", fg_color="#74a2f7", text_color="white")
        self.play_pause.grid(row=1, column=0, padx=5, pady=5)

        self.restart_btn = ctk.CTkButton(master=self, text="Restart")
        self.restart_btn.grid(row=2, column=0, padx=5, pady=5)

        self.file_volume= ctk.CTkSlider(master=self)
        self.file_volume.grid(row=4, column=0, padx=5, pady=5)

        self.file_name_label = ctk.CTkLabel(master=self, text=f"Using: {self.file_name}", font=("Roboto", 15), width=200)
        self.file_name_label.grid(row=0, column=1, padx=5, pady=5)

        self.widgets = [self.frame_title, self.play_pause, self.restart_btn, self.file_volume, self.file_name_label]

    