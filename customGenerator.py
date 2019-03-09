from AsemcoUtilities.Generator import BaseGenerator
from AsemcoUtilities.Colors import COLOR, Color
from Logitech.customTemplate import getRainbowFromMatPos, getRastaFromMatPos, wavesFromMatPos
from Logitech.logitech import NORMALIZED

from random import randint

class LogitechGenerator(BaseGenerator):
    def __init__(self, *args):
        BaseGenerator.__init__(self, *args)

        self.Shaders = [self.shaderStandard, self.shaderRainbow, self.shaderRasta, self.shaderWaves, self.shaderMono]
        self.Backgrounds = [self.backgroundStandard, self.backgroundRainbow, self.backgroundRasta, self.backgroundWaves, self.backgroundMono]
        self.Pickers = [self.pickerDefault, self.pickerRainbow, self.pickerRasta, self.pickerWaves, self.pickerMono]

    # --- RAINBOW --- #
    def pickerRainbow(self, _):
        r = randint(0, len(self._avaiableKeys) - 1)
        comb = self._avaiableKeys.pop(r)
        rainbowColor = getRainbowFromMatPos(comb)
        self._pick[comb] = Color().fromColor(rainbowColor)
        self._pick[comb].type = COLOR.FULL

    def shaderRainbow(self, key, col):
        if col.type == COLOR.FULL:
            col.half()
            col.type = COLOR.HALF
        elif col.type == COLOR.HALF:
            col.fromColor(self._backgroundColor[key])
            col.type = COLOR.DEFAULT

    def backgroundRainbow(self, key):
        colorMult = self.colorDefault.grayScale()
        rainbowColor = getRainbowFromMatPos(key)
        self._backgroundColor[key] = Color().fromColor(rainbowColor)
        self._backgroundColor[key].mult(colorMult)
        self._backgroundColor[key].type = COLOR.DEFAULT

    # --- RASTA --- #
    def pickerRasta(self, _):
        r = randint(0, len(self._avaiableKeys) - 1)
        comb = self._avaiableKeys.pop(r)
        rainbowColor = getRastaFromMatPos(comb)
        self._pick[comb] = Color().fromColor(rainbowColor)
        self._pick[comb].type = COLOR.FULL

    def shaderRasta(self, key, col):
        if col.type == COLOR.FULL:
            col.half()
            col.type = COLOR.HALF
        elif col.type == COLOR.HALF:
            col.fromColor(self._backgroundColor[key])
            col.type = COLOR.DEFAULT

    def backgroundRasta(self, key):
        colorMult = self.colorDefault.grayScale()
        rainbowColor = getRastaFromMatPos(key)
        self._backgroundColor[key] = Color().fromColor(rainbowColor)
        self._backgroundColor[key].mult(colorMult)
        self._backgroundColor[key].type = COLOR.DEFAULT

    # --- Waves --- #
    def pickerWaves(self, _):
        for r in self._avaiableKeys:
            pos = (wavesFromMatPos(r)-self._effectPos) % self.cycleLength
            self._pick[r] = Color().fromColor(self._customContainer[pos])


    def shaderWaves(self, key, col):
        return


    def backgroundWaves(self, k):
        if k == NORMALIZED[0]:
            full = self.colorFull
            half = self.colorHalf
            default = self.colorDefault
            bundle_1 = full.linear(half, self.cycleLength)
            bundle_2 = half.linear(default, self.cycleLength)
            bundle = bundle_1 + bundle_2[1:]

            self.cycleLength *= 2
            self.cycleLength -= 1

            self._customContainer = bundle

    def pickerMono(self, _):
        for r in self._avaiableKeys:
            pos = self._effectPos % self.cycleLength
            self._pick[r] = Color().fromColor(self._customContainer[pos])


    def shaderMono(self, key, col):
        return


    def backgroundMono(self, k):
        if k == NORMALIZED[0]:
            full = self.colorFull
            half = self.colorHalf
            default = self.colorDefault
            bundle_1 = full.linear(half, self.cycleLength)
            bundle_2 = half.linear(default, self.cycleLength)
            bundle = bundle_1 + bundle_2[1:]

            self.cycleLength *= 2
            self.cycleLength -= 1

            self._customContainer = bundle