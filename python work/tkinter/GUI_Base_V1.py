import customtkinter as tk

class Grid:
    def __init__(self, root, numRows, numCols):
        # Makes a fixed grid
        self.numRows = numRows
        self.numCols = numCols
        self.root = root
        self.setGrid()

    def setGrid(self):
        for i in range(self.numRows):
            self.root.rowconfigure(i, weight=1)
        for j in range(self.numCols):
            self.root.columnconfigure(j, weight=1)

class AudioViz_GUI(tk.CTk):
    """
    This is the outer program.
    """

    def __init__(self):
        super().__init__()

        #Set up application theme, color, and size
        self.geometry("750x550")
        self.minsize(width=750, height=550)
        self.title("Audio Visualizer")
        tk.set_default_color_theme("dark-blue")
        tk.set_widget_scaling(1.2)
        tk.set_appearance_mode("dark")

        #Set the program to close the application when the exit button is pressed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid = Grid(self, 18, 12)

        options = ["1","2","3"]
        self.dropdown = tk.CTkOptionMenu(self, values=options, command= (lambda x: self.dropdownCommand()))
        self.dropdown.grid(row=2, column=3, padx=0, pady=0)

    def dropdownCommand(self):
        print("Here")

    def on_closing(self):
        """
        When the exit button is pressed.
        """
        self.destroy() #End tkinter application
        sys.exit() #End program (some callbacks are imporperly handled)


#Initializes application
app = AudioViz_GUI()

#Starts application
app.mainloop()
