import customtkinter
from CTkColorPicker import *

class App(customtkinter.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cp = CTkColorPicker(master=self, width=200, command=lambda e: print(e))
        self.cp.pack(padx=10, pady=10)

app = App()
app.mainloop()