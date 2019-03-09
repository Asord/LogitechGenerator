from AsemcoUtilities.Colors import Color
from AsemcoUtilities.Maths import linearSteps, flatSteps
from Logitech.logitech import NBHUES, SLICES, SLICESLEN
from Logitech.logitechUtilities import colorFromMatPos

def _generateMatrice(nbHues, shade, steps):
    _steps = flatSteps(nbHues, shade)
    _nbCol = len(steps)
    _matrice = [Color(steps[s % _nbCol]) for s in _steps]
    return _matrice


def getRastaMatrice(nbHues):
    shade = 6
    stepColor = ["#00ff00", "#ffff00", "#ff0000"]
    _matrice = _generateMatrice(nbHues, shade, stepColor)
    return _matrice

def getFranceMatrice(nbHues):
    shade = 3
    stepColor = ["#0000ff", "#ffffff", "#ff0000"]
    _matrice = _generateMatrice(nbHues, shade, stepColor)
    return _matrice


def getRainbowMatrice(nbHues):
    hues = linearSteps(360, nbHues)
    _matrice = [Color(hue, 1, 1, True) for hue in hues]
    return _matrice

def wavesFromMatPos(key):
    for c in range(SLICESLEN):
        if key in SLICES[c]:
            return c

RASTAMAT = getRastaMatrice(NBHUES)
def getRastaFromMatPos(key): return colorFromMatPos(key, SLICES, RASTAMAT)
RAINBOWMAT = getRainbowMatrice(NBHUES)
def getRainbowFromMatPos(key): return colorFromMatPos(key, SLICES, RAINBOWMAT)
GMAT = getFranceMatrice(NBHUES)
def getGayFromMatPos(key): return colorFromMatPos(key, SLICES, GMAT)