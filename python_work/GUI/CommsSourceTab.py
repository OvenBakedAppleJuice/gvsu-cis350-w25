import customtkinter as ctk

class CommsSourceTab(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.parent = master

        self.configure(height=200, width=250)
        self.grid_propagate(False)

        #create tabs
        self.add("Live Microphone")
        self.add("System Audio")

        # add widgets on live mic
        comms_options = self.parent.ArduinoComms.getPortDescriptions()
        self.source_dropdown = ctk.CTkComboBox(master=self.tab("Arduino Comm"), values=comms_options, width=200)
        self.source_dropdown.grid(row=0, column=0, padx=20, pady=20)
    
    


        
