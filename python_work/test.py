import tkinter as tk
from tkinter import *

# use https://www.geeksforgeeks.org/create-first-gui-application-using-python-tkinter/

root = Tk()

#change title of the window
root.title("BTripleJ")

#set geometry of window
root.geometry('350x200')

# # #label widget
# a = Label(root, text = "Hello")

# # fit a object to root window
# a.pack()

# NOTE pack() and gird() cannot be used together

#new lbl using grid
lbl = Label(root, text = "cis350")
# place it in default open cell (which would be 0,0 in this case)
lbl.grid()


#render and take inputs
root.mainloop()