import customtkinter as ctk
from tkinter import filedialog
import os

class SourcesTab(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.parent = master
        self.configure(height=200, width=250)
        self.grid_propagate(False)

        self.is_mic_changed = False
        self.current_mic = None 

        self.file_path = None
        self.is_current_audio = 0 

        #create tabs
        self.add("USB Port")
        self.add("Audio Device")
        self.add("Audio MP3")

        # add widgets on USB Port
        usb_options = self.parent.ArduinoControl.getPortDescriptions()
        self.USB_source_dropdown = ctk.CTkComboBox(master=self.tab("USB Port"), values=usb_options, width=200, command=self.USBSourceDropDownEvent)
        self.USB_source_dropdown.set("None Chosen")
        self.USB_source_dropdown.grid(row=0, column=0, padx=20, pady=20)

        # add widgets on Audio Device
        device_options = self.parent.AudioControl.ListDevicesStrings()
        self.audio_source_dropdown = ctk.CTkComboBox(master=self.tab("Audio Device"), values=device_options, width=200, command=self.audioSourceDropDownEvent)
        self.audio_source_dropdown.set("Using System Default")
        self.audio_source_dropdown.grid(row=0, column=0, padx=20, pady=20)

        #add widgets on Audio MP3
        self.file_label = ctk.CTkLabel(master=self.tab("Audio MP3"), text="No file selected", anchor="w", justify="left", width=200)
        self.select_file_button = ctk.CTkButton(master=self.tab("Audio MP3"), text="Select File", fg_color="#ffe7a3", hover_color="#dbc893", text_color="black", command=self.browseFile, border_color="black")
        self.file_label.grid(row=0, column=0, padx=20, pady=0, sticky="w")
        self.select_file_button.grid(row=1, column=0, padx=20, pady=2)

    # REGION USB Port
    def USBSourceDropDownEvent(self, choice):
        # Reset the device options when a new one is selected in case they have changed
        device_options = self.parent.ArduinoControl.getPortDescriptions()
        self.USB_source_dropdown.configure(values=device_options)
        # Check device before setting it
        if choice in device_options:
            #get index of choice (device descriptions list is same length as device port name list)
            index = device_options.index(choice)
            #get portnames" COM3, COM14, etc.
            portNames = self.parent.ArduinoControl.getPorts()
            #Set current device based on port name
            self.parent.ArduinoControl.startComm(portNames[index])

    # REGION for Audio Device
    def audioSourceDropDownEvent(self, choice):
        # Reset the device options when a new one is selected in case they have changed
        device_options = self.parent.AudioControl.ListDevicesStrings()
        self.audio_source_dropdown.configure(values=device_options)
        # Check device before setting it
        if choice in device_options:
            self.is_mic_changed = True
            self.current_mic = choice
            index = device_options.index(choice)
            self.parent.AudioControl.SetDevice(index)
    

    # REGION for Audio MP3
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

    # REGION general
    # major change happened, will call pause on play_pause
    def majorChangeEvent(self):
        self.parent._play_pause_pass = False
        self.parent.play_pause.play.configure(fg_color="#20b502", text="Start", hover_color="#167d01")

    def truncate_text(self, text, max_chars=30):
        return text if len(text) <= max_chars else text[:max_chars] + "..."


        
