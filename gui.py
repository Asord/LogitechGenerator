from AsemcoUtilities.jsonTkinter import jsonWindow

from tkinter.colorchooser import askcolor
from tkinter import messagebox

from customGenerator import LogitechGenerator

from AsemcoUtilities.Colors import Color

from Logitech.logitech import KEYBOXS

from PIL import Image, ImageTk

"""
from os import system
from AsemcoUtilities.Maths import linearSteps
"""

VERSION = "0.3d"

class window(jsonWindow):
    def __init__(self):
        jsonWindow.__init__(self, "guiconfig.json")

        self._color   = "#ff0000"
        self._shadow  = "#800000"
        self._default = "#000000"

        self._binds = {
            "pickColor_0": lambda: self._pickColor(0),
            "pickColor_1": lambda: self._pickColor(1),
            "pickColor_2": lambda: self._pickColor(2),
            "updatePreview": lambda: self._startPreview(),
            "generate": lambda: self._generate(),
            "mcHelp": lambda: self._help()
        }

        self.generateGUI()


        self.Generator = LogitechGenerator()

        self.title("Logitech keyboard color generator v%s\n" % VERSION)

        ##### TODO: CLEAR DOWN #####

        self._Preview = self._config["cPreview"]

        tmp = Image.open("device.png")
        self._keyboardImage = ImageTk.PhotoImage(tmp.resize((600, 300)))

        self._Preview.create_image(300, 150, image=self._keyboardImage)

        self._previewData = {}

        self._updateAsked = False
        self._updateLastPos = 0
        self._previewSpeed = 0
        self.after(100, self._updatePreview)

    @staticmethod
    def _help():
        helpString = "Logitech keyboard color generator v%s\n" % VERSION
        helpString += "Created by Asord | CC BY-NC 3.0\n\n"
        helpString += "Avaliable arguments:\n"
        helpString += "Script Name\tDefine the script name\n"
        helpString += "File Name\tDefine the file name\n"
        helpString += "Frame length\tChange the length of each frames\n"
        helpString += "Transition type\tChange the transition for each frames\n"
        helpString += "Cycle length\tChange the number of frames per cycle\n"
        helpString += "Number of cycle\tChange the total number of cycles\n"
        helpString += "Effect\t\tChange the main effect generated:\n"
        helpString += "\nEffect 0: Simple effect\n"
        helpString += "Bright color\tThe main color of the effect\n"
        helpString += "Shadow color\tThe second color of the effect\n"
        helpString += "Default color\tThe background color of the effect\n"
        helpString += "\nEffect 1: Rainbow Effect\n"
        helpString += "Default color\tThe intensity of the background rainbow\n"

        messagebox.showinfo("Help", helpString)

    def _startPreview(self):
        self._setupGenerator()
        self._previewData.clear()
        self._previewData = self.Generator.generate(True)
        self._previewSpeed = 100*int(self._config["sLength"].get())

        self._updateAsked = True


    def _updatePreview(self):
        if self._updateAsked:

            # Clear canvas cache
            self._Preview.delete("all")
            self._Preview.create_image(300, 150, image=self._keyboardImage)

            # preview finished
            if self._updateLastPos >= len(self._previewData):
                self._updateAsked = False
                self._updateLastPos = 0

            else: # preview process
                for key, color in self._previewData[self._updateLastPos].items():
                    self._Preview.create_rectangle(KEYBOXS[key], fill=color.toHex(), stipple="gray50")
                self._updateLastPos += 1

            self.after(self._previewSpeed, self._updatePreview)

        else:
            self.after(200, self._updatePreview)


    def _setupGenerator(self):
        self.Generator.name = str(self._config["eName"].get())
        self.Generator.file = str(self._config["eOutput"].get())
        self.Generator.effectLength = int(self._config["sLength"].get())
        self.Generator.curveType = int(self._config["sType"].get())
        self.Generator.cycleLength = int(self._config["sCycle"].get())
        self.Generator.cycleCount = int(self._config["sCount"].get())
        self.Generator.effect = int(self._config["sEffect"].get())
        self.Generator.colorFull = Color(self._color)
        self.Generator.colorHalf = Color(self._shadow)
        self.Generator.colorDefault = Color(self._default)

    def _generate(self):
        if self._updateAsked:
            self._updateAsked = False
            self._updateLastPos = 0

        self._setupGenerator()
        self.Generator.generate(False)

    def _pickColor(self, col):
        color = askcolor()

        if col == 0: self._color = color[1]
        elif col == 1: self._shadow = color[1]
        else: self._default = color[1]


if __name__ == '__main__':
    win = window()
    win.mainloop()