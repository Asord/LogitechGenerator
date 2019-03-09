from json import dumps as json_dumps
from random import randint
from Logitech.logitech import NORMALIZED, NB_KEYS
from Logitech.logitechUtilities import unnormalize

from AsemcoUtilities.Colors import Color, COLOR

from sys import argv

# ---DEFAULTS--- #
NAME = "Python generated effects"
FNAME = "pythonGeneratedEffects"
ELENGTH = 3
CUTYPE = 0
CYLENGTH = 10
CYCOUNT = 4
CFULL  = Color("#ff0000")
CHALF = Color("#970000")
CDEFAULT = Color("#303030")
EFFECT = 0

# ---GENERATOR--- #
class BaseGenerator:
    def __init__(self, n=NAME, f=FNAME, el=ELENGTH, ct=CUTYPE, cl=CYLENGTH, cc=CYCOUNT, cf=CFULL, ch=CHALF, cd=CDEFAULT, e=EFFECT):
        self.name = n
        self.file = f

        self.effectLength = el
        self.curveType = ct
        self.cycleLength= cl
        self.cycleCount = cc

        self.effect = e
        self.colorFull = cf
        self.colorHalf = ch
        self.colorDefault = cd

        self.effects = []

        self._index = 0
        self._effectPos = 0

        self._avaiableKeys = []
        self._transitionList = []
        self._backgroundColor = {}
        self._pick = {}

        self._customContainer = []

        self.Shaders = [self.shaderStandard]
        self.Backgrounds = [self.backgroundStandard]
        self.Pickers = [self.pickerDefault]

    def generate(self, preview):
        if ((len(self.Shaders)-len(self.Backgrounds)) or (len(self.Shaders)-len(self.Pickers))) != 0:
            print("Error: the Shaders, Backgrounds and Pickers don't have the same length...")
            return self.effects
        if len(self.Shaders) <= self.effect:
            print("Error: effect number %d don't exist..." % self.effect)
            return self.effects

        # flush
        self._transitionList.clear()
        self._avaiableKeys.clear()
        self._backgroundColor.clear()
        self._pick.clear()
        self.effects.clear()


        self._generateBaseColor()

        for i in range(self.cycleCount):
            self._index = len(self.effects)
            self._generateCycle(preview)

        if not preview:
            file = {
                "device_layout": 5,
                "device_model": "Logitech.Gaming.Keyboard.G910",
                "device_name": "G910",
                "name": self.name,
                "transition_list": self.effects,
                "uid": "{caf2d67d-f40c-47f7-b61f-cb2f249856b0}"
            }

            with open(self.file + ".eft", "w") as fs:
                fs.write(json_dumps(file, indent=2))

        return self.effects

    def _generateCycle(self, preview):
        nbColors = NB_KEYS // self.cycleLength
        nbColors_last = NB_KEYS % self.cycleLength

        self._avaiableKeys = NORMALIZED.copy()

        for self._effectPos in range(self.cycleLength):

            if self._effectPos == 0: self._pick = self._backgroundColor.copy()
            else: self._updateShade()

            if self._effectPos == self.cycleLength: nbColors = nbColors_last

            self._pickRandom(nbColors)
            self._transitionList.append(self._realCopy(self._pick))

        self._updateFirstFrame()

        if not preview:
            for k in range(len(self._transitionList)):
                self.effects.append(
                    {
                        "color": Color().rand().toHex(),
                        "curve": self.curveType,
                        "index": self._index + k,
                        "length": self.effectLength,
                        "state": self._unserialize(self._transitionList[k])
                    }
                )
        else:
            for k in range(len(self._transitionList)):
                self.effects.append(self._transitionList[k])


    def _updateFirstFrame(self):
        self._updateShade()
        for key, color in self._pick.items():
            if color.type == 1: self._transitionList[0][key] = color

    def _generateBaseColor(self):
        for k in NORMALIZED:
            self.Backgrounds[self.effect](k)

    def _updateShade(self):
        for key, col in self._pick.items():
            self.Shaders[self.effect](key, col)

    def _pickRandom(self, nbColors):
        for i in range(nbColors):
            self.Pickers[self.effect](i)


    # Default template
    def pickerDefault(self, _):
        r = randint(0, len(self._avaiableKeys) - 1)
        comb = self._avaiableKeys.pop(r)
        self._pick[comb] = Color().fromColor(self.colorFull)
        self._pick[comb].type = COLOR.FULL

    def shaderStandard(self, _, col):
        if col.type == COLOR.FULL:
            col.fromColor(self.colorHalf)
            col.type = COLOR.HALF
        elif col.type == COLOR.HALF:
            col.fromColor(self.colorDefault)
            col.type = COLOR.DEFAULT

    def backgroundStandard(self, key):
        self._backgroundColor[key] = Color().fromColor(self.colorDefault)
        self._backgroundColor[key].type = COLOR.DEFAULT

    @staticmethod
    def _realCopy(dictionary):
        new = {}
        for k, v in dictionary.items():
            new[k] = Color(v.toHex())
            new[k].type = v.type
        return new

    @staticmethod
    def _unserialize(dic):
        state = {"1": {}, "4": {}, "10": {}}
        for k, v in dic.items():
            space, key = unnormalize(k)
            state[space][key] = v.toHex()
        return state

def _printHelp():
    helpString =  "Python Logitech color sheme generator v0.2a\n"
    helpString += "Avaliable arguments:\n"
    helpString += "-name   | -n\tChange script name (any ASCII)\n"
    helpString += "-output | -o\tEdit the file name (any ASCII)\n"
    helpString += "-length | -l\tEdit frame length (1 to 20)\n"
    helpString += "-type   | -t\tAffect the curve type (0 to 9)\n"
    helpString += "-cycle  | -c\tNumber of frames per cycle (1 to 52)\n"
    helpString += "-count  | -k\tNumber of cycles (1 to any)\n"
    helpString += "-effect | -e\tEffect to create:\n"
    helpString += "\tSimple effect (single color): 0\n\tParams:"
    helpString += "\t-color  | -q\tColor of effect (#rrggbb)\n"
    helpString += "\t-shadow | -s\tShadow color of the effect (#rrggbb)\n"
    helpString += "\t-default| -d\tDefault color of all keys (#rrggbb)\n"
    helpString += "\tRainbow Effect (rainbow color): 1\n\tParams:"
    helpString += "\t-default| -d\tBackground intensity grayscaled (#rrggbb)\n"
    helpString += "-help   | -h\tThis helpfull message\n"

    print(helpString)

def generate(args, preview=False):
    generator = BaseGenerator()

    for i in range(0, len(args), 2):
        arg = args[i]
        param = args[i+1]

        if arg == "-name" or arg == "-n":
            generator.name = str(param)
        elif arg == "-output" or arg == "-o":
            generator.file = str(param)

        elif arg == "-length" or arg == "-l":
            generator.effectLength = int(param)
        elif arg == "-type" or arg == "-t":
            generator.curveType = int(param)
        elif arg == "-cycle" or arg == "-c":
            generator.cycleLength = int(param)
        elif arg == "-count" or arg == "-k":
            generator.cycleCount = int(param)

        elif arg == "-effect" or arg == "-e":
            generator.effect = int(param)

        elif arg == "-color" or arg == "-q":
            generator.colorFull = Color(str(param))
        elif arg == "-shadow" or arg == "-s":
            generator.colorHalf = Color(str(param))
        elif arg == "-default" or arg == "-d":
            generator.colorDefault = Color(str(param))

        elif arg == "-help" or arg == "-h" or arg == "/?":
            _printHelp()
            quit()
        else:
            print("unreconized argument: %s" % arg)
            quit()

    generator.generate(preview)

if __name__ == "__main__":
    generate(argv[1:])

