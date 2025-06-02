import customtkinter as ctk
import pyaudio


class AudioFilePlayer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(height=200, width=600)

        self.file_path = None
        self.file_name = None

        # add items to frame
        self.frame_title = ctk.CTkLabel(master=self, text="MP3 File Player", font=("Roboto", 15))
        self.frame_title.grid(row=0, column=0, padx=5, pady=5)

        self.play_pause = ctk.CTkButton(master=self, text="Play")
        self.play_pause.grid(row=1, column=0, padx=5, pady=5)

        self.restart_btn = ctk.CTkButton(master=self, text="Restart")
        self.restart_btn.grid(row=2, column=0, padx=5, pady=5)

        self.file_volume= ctk.CTkSlider(master=self)
        self.file_volume.grid(row=4, column=0, padx=5, pady=5)

        self.file_name_label = ctk.CTkLabel(master=self, text=f"Using: {self.file_name}", font=("Roboto", 15), width=200)
        self.file_name_label.grid(row=0, column=1, padx=5, pady=5)


        # start disabled
        self.disabledAllWidgets()





    def enableAllWidgets(self):
        for widget in self.winfo_children():
            try:
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="#ffffff")
                else:
                    widget.configure(state="enabled")
            except Exception:
                pass    #some widgets like label dont have state

    def disabledAllWidgets(self):
        for widget in self.winfo_children():
            try:
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text_color="#828282")
                else:
                    widget.configure(state="disabled")
            except Exception:
                pass    #some widgets like label dont have state

    