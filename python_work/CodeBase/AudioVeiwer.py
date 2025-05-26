import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PlotBins:
    """
    This is usually only called when an update occurs. It shows a notes repeated pattern, including harmonics.
    """
    def __init__(self, root):
        self.root = root

        bins = [0 for i in range(16)]
        self.x_pos = [(i+1) for i in range(16)]

        #fig, ax = plt.subplots(dpi=DPI)
        fig, self.ax = plt.subplots()
        self.ax.set_title("Histogram of Frequency.")

        self.barContainer = self.ax.bar(self.x_pos, bins, color='skyblue')

        self.ax.autoscale_view()

        # Remove x-axis and y-axis ticks and labels
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_ylabel("Volume")
        self.ax.set_xlabel("Frequency")
        self.ax.set_ylim(0, 2000000)
        self.ax.set_xlim(0, 17)

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()

    def plotBins(self, bins):
        for patch in self.barContainer.patches:
            patch.remove()
        
        self.barContainer = self.ax.bar(self.x_pos, bins, color='blue')

        self.canvas.draw()
        return self.canvas.get_tk_widget()
