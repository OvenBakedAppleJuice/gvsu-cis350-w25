import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np




class PlotBins:
    """
    This is usually only called when an update occurs. It shows a notes repeated pattern, including harmonics.
    """
    def __init__(self, root):
        self.root = root

    def plotBins(self, bins):
        #fig, ax = plt.subplots(dpi=DPI)
        fig, ax = plt.subplots()
        ax.set_title("Histogram of Frequency.")
        ax.hist(bins)
        ax.autoscale_view()

        # Remove x-axis and y-axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylabel("Volume")
        ax.set_xlabel("Frequency")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        return canvas.get_tk_widget()
        