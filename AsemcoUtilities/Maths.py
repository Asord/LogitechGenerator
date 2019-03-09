def linearSteps(number, nbSlices, precision=1):
    
    if number == 0:
        _steps = [0 for _ in range(nbSlices)]
        
    else:    
        _nbFrames = nbSlices - 1
        
        numberNormalized = int(number*precision)
        _dIncrement = int(numberNormalized / _nbFrames)
        
        _steps = [k/precision for k in range(0, numberNormalized, _dIncrement)]

        if numberNormalized % _nbFrames == 0: _steps.append(numberNormalized/precision)
        else: _steps[-1] = numberNormalized/precision

    return _steps

def deltaBase(val1, val2):
    delta = val1 -  val2
    if delta < 0:
        delta *= -1
        base = -1
    else:
        base = 1
    return delta, base

def flatSteps(number, slices):
    steps = number//slices
    last = steps+number%slices

    _lst = []
    for p in range(slices):
        if p == slices-1:
            [_lst.append(p) for _ in range(last)]
        else:
            [_lst.append(p) for _ in range(steps)]

    return _lst

if __name__ == '__main__':
    flatSteps(24, 6)