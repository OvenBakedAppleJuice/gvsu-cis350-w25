import customtkinter as ctk
from CTkColorPicker import *

class ColorSelectFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self._hex = "#ffffff"
        self._hsv = 0
        self._intColor = 0

        self.color_picker = CTkColorPicker(self, width=230, height=160, command=self.colorChanged)
        self.color_picker.pack(padx=1, pady=1)

    def colorChanged(self, new_value):
        self._hex = new_value
        hexNoHashtag = self._hex[1:]
        self._intColor = int(hexNoHashtag, 16) #converts sting of base 16 to int
        self._hsv = self.hex_to_hsv(self._hex)

    def hex_to_hsv(self, hex_color):
        """Convert a hex color (e.g., '#FF5733') to HSV (Hue [0–360], Saturation/Value [0–1])"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0

        max_c = max(r, g, b)
        min_c = min(r, g, b)
        delta = max_c - min_c

        # Hue calculation
        if delta == 0:
            h = 0
        elif max_c == r:
            h = (60 * ((g - b) / delta) + 360) % 360
        elif max_c == g:
            h = (60 * ((b - r) / delta) + 120) % 360
        elif max_c == b:
            h = (60 * ((r - g) / delta) + 240) % 360

        # Saturation
        s = 0 if max_c == 0 else delta / max_c

        # Value
        v = max_c

        return (h, s, v)
