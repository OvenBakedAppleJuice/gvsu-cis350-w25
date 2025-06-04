import customtkinter as ctk
import pyaudio
from tkinter import filedialog
import os

class AudioSourceTab(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.parent = master

        self.is_mic_changed = False
        self.current_mic = None

        self.file_path = None
        self.is_current_audio = 0 

        self.configure(height=200, width=220)

        #create tabs
        self.add("Live Microphone")
        self.add("System Audio")

        # add widgets on live mic
        mic_options = self.GetListOfMics()
        default_mic = self.GetDefaultMic()
        self.source_dropdown = ctk.CTkComboBox(master=self.tab("Live Microphone"), values=mic_options, width=220)
        self.source_dropdown.set(default_mic)
        self.current_mic = default_mic
        self.source_dropdown.grid(row=0, column=0, padx=20, pady=20)

        #add widgets on System Audio
        self.file_label = ctk.CTkLabel(master=self.tab("System Audio"), text="No file selected", anchor="w", justify="left", width=200)
        self.select_file_button = ctk.CTkButton(master=self.tab("System Audio"), text="Select File", fg_color="#ffe7a3", hover_color="#dbc893", text_color="black", command=self.browseFile, border_color="black")
        self.file_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
        self.select_file_button.grid(row=1, column=0, padx=20, pady=2)

        self.current_checkbox = ctk.CTkCheckBox(master=self.tab("System Audio"), text="Use current system audio", command=self.currentCheckboxEvent)
        self.current_checkbox.grid(row=2, column=0, padx=20, pady=3)

    # REGION for Live Microphone
    def sourceDropDownEvent(self, choice):
        self.is_mic_changed = True
        self.current_mic = choice

    # returns list of audio inputs as strings with there index and name
    def GetListOfMics(self):
        devices = []
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                devices.append(f"{i}: {info['name']}")
        return devices
        

    def GetDefaultMic(self):
        p = pyaudio.PyAudio()
        def_in = p.get_default_input_device_info()
        return f"{def_in['index']}: {def_in['name']}"
    

    # REGION for System Audio

    def browseFile(self):
        self.majorChangeEvent()
        file_path = filedialog.askopenfilename(
            title="Select an MP3 file",
            filetypes=[("MP3 Files", "*.mp3")],
            defaultextension=".mp3"
        )
        if file_path:
            print("User Selected file: ", file_path)
            self.file_path = file_path
            self.enabledAudioFilePlayer(self.file_path)

    def enabledAudioFilePlayer(self, file_path: str):
        print(f"======Path {file_path}")
        self.parent.audio_file_player.startUpPlayerFromPath(file_path)
        text = os.path.basename(file_path)
        text = self.truncate_text(text)
        self.file_label.configure(text=text)

    def currentCheckboxEvent(self):
        self.majorChangeEvent()
        self.is_current_audio = self.current_checkbox.get()
        # disable file select if true
        if self.is_current_audio == 1:
            self.select_file_button.configure(state="disabled")
        else:
            self.select_file_button.configure(state="enabled")


    # REGION general
    # major change happened, will call pause on play_pause
    def majorChangeEvent(self):
        self.parent._play_pause_pass = False
        self.parent.play_pause.play.configure(fg_color="#20b502", text="Start", hover_color="#167d01")

    def truncate_text(self, text, max_chars=30):
        return text if len(text) <= max_chars else text[:max_chars] + "..."


        
