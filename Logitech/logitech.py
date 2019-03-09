from json import loads
from Logitech.logitechUtilities import getNormalized, getKeyBoxs

#---CONFIG---"
_CONFIGFILE = "logitech/logitechConfig.json"
with open(_CONFIGFILE, "r") as fs: data = loads(fs.read())

#---DATA---"
KEYS = data["keyConfig"]
NB_KEYS = data["nbKeys"]

NBHUES = data["hues"]
SLICES = data["slices"]
SLICESLEN = len(data["slices"])

NORMALIZED = getNormalized(KEYS)
KEYBOXS = getKeyBoxs()


