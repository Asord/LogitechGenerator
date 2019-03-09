from json import loads

def getNormalized(keys):
    _Normalized = []
    for key, values in keys.items():
        for value in values:
            _Normalized.append(key + "_" + value)
    return _Normalized


"""
def getSVGKeycode(base, combo):
    if len(combo) == 1:
        combo = '0' + combo
    _key = ""
    if base == "1":
        _key = "0x" + combo
    elif base == "4":
        _key = "0x1" + combo
    return _key
"""

def unnormalize(normalized):
    return tuple(normalized.split("_"))

def colorFromMatPos(key, background, matrice):
    for c in range(len(background)):
        if key in background[c]:
            return matrice[c]

def getKeyBoxs():
    with open("logitech/keybox.json", "r") as fs:
        data = loads(fs.read())
        return data