from math import floor
from random import randint
from AsemcoUtilities.Maths import linearSteps

class COLOR:
    FULL = 0
    HALF = 1
    DEFAULT = 2

class Color:
    def __init__(self, red=0, green=0, blue=0, HSV=False):

        self._red = red
        self._green = green
        self._blue = blue

        self.type = COLOR.FULL

        if type(red) == str: self.fromHex(red)
        elif HSV: self.fromHSV(red, green, blue)
        elif red > 255: self.fromInt(red)

    def rand(self):
        self._red = randint(0, 255)
        self._green = randint(0, 255)
        self._blue = randint(0, 255)
        return self

    def zero(self):
        self._red = 0
        self._green = 0
        self._blue = 0
        return self

    def copy(self):
        return Color(self._red, self._green, self._blue)

    def fromColor(self, other):
        self.fromInt(other.toInt())
        return self

    def mult(self, force):
        self._red -= int(self._red*force)
        self._green -= int(self._green*force)
        self._blue -= int(self._blue*force)
        return self

    def grayScale(self):
        gray = (self._red+self._green+self._blue) / 3
        return 1- gray/255


    def half(self):
        self._red //= 2
        self._green //= 2
        self._blue //= 2
        return self

    def fromHex(self, hexValue):
        hexValue = hexValue.replace("#", "")
        self._red = int(hexValue[0:2], 16)
        self._green = int(hexValue[2:4], 16)
        self._blue = int(hexValue[4:6], 16)
        return self

    def fromInt(self, integer):
        self._blue = integer & 255
        self._green = (integer >> 8) & 255
        self._red = (integer >> 16) & 255
        return self



    def fromRGB(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue
        return self

    def fromHSV(self, h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)

        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        self._red, self._green, self._blue = int(r * 255), int(g * 255), int(b * 255)
        return self

    def linear(self, other, length):
        sh,ss,sv = self.toHSV()
        oh,os,ov = other.toHSV()

        dh = sh-oh
        ds = ss-os
        dv = sv-ov

        hSign = -1 if dh > 0 else 1
        sSign = -1 if ds > 0 else 1
        vSign = -1 if dv > 0 else 1

        _linearH = linearSteps(dh, length, 1000)
        _linearS = linearSteps(ds, length, 1000)
        _linearV = linearSteps(dv, length, 1000)

        _color = []
        for i in range(length):
            h = sh + (_linearH[i]*hSign)
            s = ss + (_linearS[i]*sSign)
            v = sv + (_linearV[i]*vSign)
            _color.append(Color(h, s, v, True))

        return _color

    def toHSV(self):
        r, g, b = self._red / 255.0, self._green / 255.0, self._blue / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360

        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v

    def toHex(self):
        rh = format(self._red, '02x')
        gh = format(self._green, '02x')
        bh = format(self._blue, '02x')
        return '#%s%s%s' % (rh, gh, bh)

    def toInt(self):
        integer = self._blue
        integer += self._green << 8
        integer += self._red << 16
        return integer

    def toRGB(self):
        return self._red, self._green, self._blue

    def __repr__(self):
        return "color[%d] (%s, %s, %s)" % (self.type, self._red, self._green, self._blue)

    def __str__(self):
        return self.__repr__()
