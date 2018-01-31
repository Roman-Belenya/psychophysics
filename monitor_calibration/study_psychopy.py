class GammaCalculator(object):
    """Class for managing gamma tables

    **Parameters:**

    - inputs (required)= values at which you measured screen luminance either
        in range 0.0:1.0, or range 0:255. Should include the min
        and max of the monitor

    Then give EITHER "lums" or "gamma":

        - lums = measured luminance at given input levels
        - gamma = your own gamma value (single float)
        - bitsIN = number of values in your lookup table
        - bitsOUT = number of bits in the DACs

    myTable.gammaModel
    myTable.gamma

    """

    def __init__(self,
                 inputs=(),
                 lums=(),
                 gamma=None,
                 bitsIN=8,  # how values in the LUT
                 bitsOUT=8,
                 eq=1):  # how many values can the DACs output
        super(GammaCalculator, self).__init__()
        self.lumsInitial = list(lums)
        self.inputs = inputs
        self.bitsIN = bitsIN
        self.bitsOUT = bitsOUT
        self.eq = eq
        # set or or get input levels
        if len(inputs) == 0 and len(lums) > 0:
            self.inputs = DACrange(len(lums))
        else:
            self.inputs = list(inputs)

        # set or get gammaVal
        # user is specifying their own gamma value
        if len(lums) == 0 or gamma != None:
            self.gamma = gamma
        elif len(lums) > 0:
            self.min, self.max, self.gammaModel = self.fitGammaFun(
                self.inputs, self.lumsInitial)
            if eq == 4:
                self.gamma, self.a, self.k = self.gammaModel
                self.b = (lums[0] - self.a)**(old_div(1.0, self.gamma))
            else:
                self.gamma = self.gammaModel[0]
                self.a = self.b = self.k = None
        else:
            raise AttributeError("gammaTable needs EITHER a gamma value"
                                   " or some luminance measures")

    def fitGammaFun(self, x, y):
        """
        Fits a gamma function to the monitor calibration data.

        **Parameters:**
            -xVals are the monitor look-up-table vals, either 0-255 or 0.0-1.0
            -yVals are the measured luminances from a photometer/spectrometer

        """
        minGamma = 0.8
        maxGamma = 20.0
        gammaGuess = 2.0
        y = numpy.asarray(y)
        minLum = y[0]
        maxLum = y[-1]
        if self.eq == 4:
            aGuess = old_div(minLum, 5.0)
            kGuess = (maxLum - aGuess)**(old_div(1.0, gammaGuess)) - aGuess
            guess = [gammaGuess, aGuess, kGuess]
            bounds = [[0.8, 5.0], [0.00001, minLum - 0.00001], [2, 200]]
        else:
            guess = [gammaGuess]
            bounds = [[0.8, 5.0]]
        # gamma = optim.fmin(self.fitGammaErrFun, guess, (x, y, minLum, maxLum))
        # gamma = optim.fminbound(self.fitGammaErrFun,
        #    minGamma, maxGamma,
        #    args=(x,y, minLum, maxLum))
        params = optim.fmin_tnc(self.fitGammaErrFun, numpy.array(guess),
                                approx_grad=True,
                                args=(x, y, minLum, maxLum),
                                bounds=bounds, messages=0)
        return minLum, maxLum, params

    def fitGammaErrFun(self, params, x, y, minLum, maxLum):
        """Provides an error function for fitting gamma function

        (used by fitGammaFun)
        """
        if self.eq == 4:
            gamma, a, k = params
            _m = gammaFun(x, minLum, maxLum, gamma, eq=self.eq, a=a, k=k)
            model = numpy.asarray(_m)
        else:
            gamma = params[0]
            _m = gammaFun(x, minLum, maxLum, gamma, eq=self.eq)
            model = numpy.asarray(_m)
        SSQ = numpy.sum((model - y)**2)
        return SSQ




def gammaFun(xx, minLum, maxLum, gamma, eq=1, a=None, b=None, k=None):
    """Returns gamma-transformed luminance values.
    y = gammaFun(x, minLum, maxLum, gamma)

    a and b are calculated directly from minLum, maxLum, gamma

    **Parameters:**

        - **xx** are the input values (range 0-255 or 0.0-1.0)
        - **minLum** = the minimum luminance of your monitor
        - **maxLum** = the maximum luminance of your monitor (for this gun)
        - **gamma** = the value of gamma (for this gun)

    """
    # scale x to be in range minLum:maxLum
    xx = numpy.array(xx, 'd')
    maxXX = max(xx)
    if maxXX > 2.0:
        # xx = xx * maxLum / 255.0 + minLum
        xx = old_div(xx, 255.0)
    else:  # assume data are in range 0:1
        pass
        # xx = xx * maxLum + minLum

    # eq1: y = a + (b*xx)**gamma
    # eq2: y = (a + b * xx)**gamma
    # eq4: y = a + (b + k*xx)**gamma  # Pelli & Zhang 1991
    if eq == 1:
        a = minLum
        b = (maxLum - a)**(old_div(1, gamma))
        yy = a + (b * xx)**gamma
    elif eq == 2:
        a = minLum**(old_div(1, gamma))
        b = maxLum**(old_div(1, gamma)) - a
        yy = (a + b * xx)**gamma
    elif eq == 3:
        # NB method 3 was an interpolation method that didn't work well
        pass
    elif eq == 4:
        nMissing = sum([a is None, b is None, k is None])
        # check params
        if nMissing > 1:
            msg = "For eq=4, gammaFun needs 2 of a, b, k to be specified"
            raise AttributeError(msg)
        elif nMissing == 1:
            if a is None:
                a = minLum - b**(old_div(1.0, gamma))  # when y=min, x=0
            elif b is None:
                if a >= minLum:
                    b = 0.1**(old_div(1.0, gamma))  # can't take inv power of -ve
                else:
                    b = (minLum - a)**(old_div(1.0, gamma))  # when y=min, x=0
            elif k is None:
                k = (maxLum - a)**(old_div(1.0, gamma)) - b  # when y=max, x=1
        # this is the same as Pelli and Zhang (but different inverse function)
        yy = a + (b + k * xx)**gamma  # Pelli and Zhang (1991)

    return yy


def gammaInvFun(yy, minLum, maxLum, gamma, b=None, eq=1):
    """Returns inverse gamma function for desired luminance values.
    x = gammaInvFun(y, minLum, maxLum, gamma)

    a and b are calculated directly from minLum, maxLum, gamma
    **Parameters:**

        - **xx** are the input values (range 0-255 or 0.0-1.0)
        - **minLum** = the minimum luminance of your monitor
        - **maxLum** = the maximum luminance of your monitor (for this gun)
        - **gamma** = the value of gamma (for this gun)
        - **eq** determines the gamma equation used;
            eq==1[default]: yy = a + (b * xx)**gamma
            eq==2: yy = (a + b*xx)**gamma

    """

    # x should be 0:1
    # y should be 0:1, then converted to minLum:maxLum

    # eq1: y = a + (b * xx)**gamma
    # eq2: y = (a + b * xx)**gamma
    # eq4: y = a + (b + kxx)**gamma
    if max(yy) == 255:
        yy = old_div(numpy.asarray(yy, 'd'), 255.0)
    elif min(yy) < 0 or max(yy) > 1:
        logging.warning(
            'User supplied values outside the expected range (0:1)')
    else:
        yy = numpy.asarray(yy, 'd')

    if eq == 1:
        xx = numpy.asarray(yy)**(old_div(1.0, gamma))
    elif eq == 2:
        yy = numpy.asarray(yy) * (maxLum - minLum) + minLum
        a = minLum**(old_div(1, gamma))
        b = maxLum**(old_div(1, gamma)) - a
        xx = old_div((yy**(old_div(1, gamma)) - a), b)
        maxLUT = old_div((maxLum**(old_div(1, gamma)) - a), b)
        minLUT = old_div((minLum**(old_div(1, gamma)) - a), b)
        xx = old_div(xx, (maxLUT - minLUT)) - minLUT
    elif eq == 3:
        # NB method 3 was an interpolation method that didn't work well
        pass
    elif eq == 4:
        # this is not the same as Zhang and Pelli's inverse
        # see http://www.psychopy.org/general/gamma.html for derivation
        a = minLum - b**gamma
        k = (maxLum - a)**(old_div(1., gamma)) - b
        xx = old_div((((1 - yy) * b**gamma + yy * (b + k)**gamma)**(old_div(1, gamma)) - b), k)

    # then return to range (0:1)
    # xx = xx / (maxLUT - minLUT) - minLUT
    return xx
