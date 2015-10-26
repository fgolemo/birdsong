import math


class AlphaBeta2Dat():
    """ Translate an input file of alpha and beta values to DAT.

    This file is a direct port of the amazing C code used to synthesize
    Zebra Finch sounds, created by the Dynamic Systems lab at Universidad de Buenos Aires.

    This class will read two files, for alpha and beta values (alpha = labia tension,
    beta = air pressure). The output is a DAT file that can be compiled to WAV (code for that is provided by
    the Buenos Aires group).

    Frankly I have no remote idea what's happening in this file. It's random variable names that I just
    copied from the original file and random crazy calculations without any clear purpose. Yet this code works almost
    as good as the original code (not in speed but in function). The whole purpose of this port was to better
    understand what's happening in this weird mess of code, but this is too big of a feat for any single man.

    Instead the current function of this class is to serve as precursor for what will later become part of the
    Birdsond Architecture, where it will be used a blackbox.

    For usage of this file, please see the main function for an example.

    :param alphaFile: path to the file with the alpha values
    :param envelopeFile: path to the file with the envelope (beta) values
    """

    def __init__(self, alphaBetaStream, outputStream):
        self.alphaBetaStream = alphaBetaStream
        self.outputStream = outputStream
        self.defineConstants()
        self.birdstate = BirdState()
        self.initV()
        self.initLoopVars()
        self.initTau()

    def defineConstants(self):
        self.Hertz = 44100
        self.IA = 16807
        self.IM = 2147483647
        self.AM = (1.0 / self.IM)
        self.IQ = 127773
        self.IR = 2836
        self.NTAB = 32
        self.NDIV = (1 + (self.IM - 1) / self.NTAB)
        self.EPS = 1.2e-7
        self.RNMX = (1.0 - self.EPS)
        self.N_NAME1_AUX = 30
        self.c = 35000

    def initLoopVars(self):
        self.stepping = 20
        self.tiempot = 0.0
        self.tcount = 0
        self.tnoise = 0
        self.atenua = 1
        self.dt = 1. / (self.Hertz * self.stepping)
        self.updateAnchos(True)
        self.ancho3 = self.ancho2
        self.largo1 = 1.5
        self.largo2 = 1.5
        self.largo3 = 1.0
        self.idum = -1

    def updateAnchos(self, firstRun):
        self.ancho1 = self.birdstate.Ancho1
        self.ancho2 = self.birdstate.Ancho2
        if firstRun:
            self.ancho3 = self.ancho2
        self.r12 = (self.ancho1 - self.ancho2) / (self.ancho1 + self.ancho2)
        self.r21 = -self.r12
        self.r23 = (self.ancho2 - self.ancho3) / (self.ancho2 + self.ancho3)
        self.r32 = -self.r23
        self.t12 = 1 + self.r12
        self.t21 = 1 + self.r21
        self.t23 = 1 + self.r23
        self.t32 = 1 + self.r32

    def initTau(self):
        self.tau1 = self.rint(self.largo1 / (self.c * self.dt))
        self.tau2 = self.rint(self.largo2 / (self.c * self.dt))
        self.tau3 = self.rint(self.largo3 / (self.c * self.dt))

        self.maxtau = self.tau3
        if (self.tau1 >= self.tau2 and self.tau1 >= self.tau3):
            self.maxtau = self.tau1
        if (self.tau2 >= self.tau1 and self.tau2 >= self.tau3):
            self.maxtau = self.tau2

        self.t = int(self.maxtau)
        self.taux = 0

        self.a = [0] * int(self.t)
        self.bf = [0] * int(self.t)
        self.bb = [0] * int(self.t)
        self.cf = [0] * int(self.t)
        self.cb = [0] * int(self.t)
        self.df = [0] * int(self.t)
        self.db = [0] * int(self.t)

    def initV(self):
        self.v = [
            0.000000000005,
            0.00000000001,
            0.000000000001,
            0.00000000001,
            0.000000000001,
            0.0000000000045,
            0.000000000000001,
            0.0,
            0.1,
            0.0
        ]

    @staticmethod
    def rint(num):
        """Rounds toward the even number if equidistant"""
        return int(round(num + (num % 2 - 1 if (num % 1 == 0.5) else 0)))

    def ran1(self, idum):
        iv = [0] * self.NTAB

        if (0 - idum) < 1:
            idum = 1
        else:
            idum = 0 - idum

        for j in range(self.NTAB, 0, -1):

            k = idum / self.IQ
            idum = self.IA * (idum - k * self.IQ) - self.IR * k
            if idum < 0:
                idum += self.IM
            if j < self.NTAB:
                iv[j] = idum

        iy = iv[0]
        k = idum / self.IQ
        idum = self.IA * (idum - k * self.IQ) - self.IR * k
        if idum < 0:
            idum += self.IM
        j = iy / self.NDIV
        iy = iv[j]
        iv[j] = idum
        temp = self.AM * iy
        if temp > self.RNMX:
            return (idum, self.RNMX)
        else:
            return (idum, temp)

    def rk4(self, h, n):
        h0 = [0] * 260

        dt2 = self.dt / 2
        dt6 = self.dt / 6

        for i in range(n):
            h0[i] = h[i]

        k1 = self.takens(h0)
        for i in range(n):
            h0[i] = h[i] + dt2 * k1[i]

        k2 = self.takens(h0)
        for i in range(n):
            h0[i] = h[i] + dt2 * k2[i]

        k3 = self.takens(h0)
        for i in range(n):
            h0[i] = h[i] + self.dt * k3[i]

        k4 = self.takens(h0)
        for i in range(n):
            h0[i] = h[i] + self.dt * k4[i]

        for i in range(n):
            h[i] = h[i] + dt6 * (2.0 * (k2[i] + k3[i]) + k1[i] + k4[i])

        return h

    def takens(self, v):

        x = v[0]
        y = v[1]
        i1 = v[2]
        i2 = v[3]
        i3 = v[4]
        x2 = v[5]
        y2 = v[6]
        x3 = v[8]
        y3 = v[9]

        dv = [0] * 10

        dv[0] = y
        dv[1] = self.birdstate.alfa1 * self.birdstate.gm ** 2 + \
                self.birdstate.beta1 * self.birdstate.gm ** 2 * x - \
                self.birdstate.gm ** 2 * x ** 3 - \
                self.birdstate.gm * x ** 2 * y + \
                self.birdstate.gm ** 2 * x ** 2 - \
                self.birdstate.gm * x * y

        dv[2] = i2
        dv[3] = -self.birdstate.s1overLG * self.birdstate.s1overCH * i1 - \
                self.birdstate.rdis * (self.birdstate.s1overLB + self.birdstate.s1overLG) * i2 + \
                i3 * (self.birdstate.s1overLG * self.birdstate.s1overCH -
                      self.birdstate.rdis * self.birdstate.RB * self.birdstate.s1overLG * self.birdstate.s1overLB) + \
                self.birdstate.s1overLG * self.birdstate.forcing2 + \
                self.birdstate.rdis * self.birdstate.s1overLG * self.birdstate.s1overLB * self.birdstate.forcing1

        dv[4] = -(1 / self.birdstate.s1overLG) * self.birdstate.s1overLB * i2 - \
                self.birdstate.RB * self.birdstate.s1overLB * i3 + \
                self.birdstate.s1overLB * self.birdstate.forcing1

        dv[5] = y2
        dv[6] = self.birdstate.alfa2 * self.birdstate.gm ** 2 + \
                self.birdstate.beta2 * self.birdstate.gm ** 2 * x2 - \
                self.birdstate.gm ** 2 * x2 ** 3 - \
                self.birdstate.gm * x2 ** 2 * y2 + \
                self.birdstate.gm ** 2 * x2 ** 2 - \
                self.birdstate.gm * x2 * y2
        dv[7] = 0.0

        dv[8] = y3
        dv[9] = -1.0 * self.birdstate.gamma2 ** 2 * self.birdstate.alfa3 * x3 + \
                self.birdstate.gamma2 * self.birdstate.beta3 * y3 - \
                self.birdstate.gamma3 * self.birdstate.gamma2 * 2.0 * 40 ** 2 * x3 ** 2 * y3

        return dv

    def mainLoop(self):
        # print "alpha,beta"
        while self.v[1] > -5000000:
            if len(self.db) == self.t-1:
                self.dbold = self.db[self.t]
            else:
                self.dbold = 0

            self.a.append(0.5 * (1.01 * (1.0 * (self.birdstate.A1 * self.v[1] +
                                                self.birdstate.A2 * self.v[6] +
                                                self.birdstate.A3 * self.v[9] / 10.))) + \
                          self.bb[self.t - self.tau1])
            self.bb.append(self.r12 * self.a[self.t - self.tau1] + \
                           self.t21 * self.cb[self.t - self.tau2])
            self.bf.append(self.t12 * self.a[self.t - self.tau1] + \
                           self.r21 * self.cb[self.t - self.tau2])

            self.cb.append(self.r23 * self.bf[self.t - self.tau2] + \
                           self.t32 * self.db[self.t - self.tau3])
            self.cf.append(self.t23 * self.bf[self.t - self.tau2] + \
                           self.r32 * self.db[self.t - self.tau3])
            self.db.append(-self.birdstate.r * self.cf[self.t - self.tau3])

            self.ddb = (self.db[self.t] - self.dbold) / self.dt
            self.birdstate.forcing1 = self.db[self.t]
            self.birdstate.forcing2 = self.ddb

            self.tiempot += self.dt

            self.birdstate.gm = 24000.0

            self.updateAnchos(False)

            self.v = self.rk4(self.v, 10)
            self.birdstate.noise = 0
            self.preout = self.birdstate.RB * self.v[4]

            if self.taux == 20:
                self.outputStream(self.preout * 10)
                (self.birdstate.amplitud, self.birdstate.beta1) = self.alphaBetaStream()
                if self.birdstate.amplitud == False:  # input stream is over
                    break

                self.taux = 0

            self.taux += 1

            if self.tiempot > 0.00:

                self.birdstate.alfa1 = -0.15 - 0.00 * self.birdstate.amplitud
                self.birdstate.alfa2 = 0.15
                self.birdstate.beta2 = 0.1
                self.birdstate.r = 0.1
                self.idum, randomNoise = self.ran1(self.idum)
                self.birdstate.noise = 0.21 * (randomNoise - 0.5)
                self.birdstate.beta1 = self.birdstate.beta1 + 0.01 * self.birdstate.noise
                self.birdstate.s1overCH = (360 / 0.8) * 1e08
                self.birdstate.s1overLB = 1e-04
                self.birdstate.s1overLG = 1.0 / 82
                self.birdstate.RB = 0.5 * 1e07

                self.birdstate.rdis = 600000.0
                self.birdstate.A1 = self.birdstate.amplitud + 0.5 * self.birdstate.noise

                if self.tiempot > 0.1 and self.tiempot < 0.165:
                    self.birdstate.A1 = math.sqrt(self.birdstate.amplitud) + 10.5 * self.birdstate.noise

                if self.tiempot > 0.215 and self.tiempot < 0.315:
                    self.birdstate.A1 = math.sqrt(self.birdstate.amplitud) + 10.5 * self.birdstate.noise

                if self.tiempot > 0.3425 and self.tiempot < 0.499:
                    self.birdstate.A1 = math.sqrt(self.birdstate.amplitud) + 10.5 * self.birdstate.noise

                if self.tiempot > 0.214 and self.tiempot < 0.255:
                    self.birdstate.A1 = self.birdstate.A1 / 2.0

                self.birdstate.A2 = 0.0
                self.birdstate.A3 = 0.0

            self.t += 1


class BirdState():
    A1 = 0.0
    A2 = 0.0
    A3 = 0.0
    alfa1 = 0.0
    alfa2 = 0.15
    alfa3 = 10000000.0
    amplitud = 0.0
    Ancho1 = 0.2
    Ancho2 = 0.2
    Ancho3 = 0.2
    beta1 = 0.0
    beta2 = 0.15
    beta3 = -200.0
    forcing1 = 0.0
    forcing2 = 0.0
    gamma2 = 1.0
    gamma3 = 1.0
    gm = 0.0
    LGoverLB = 0.0
    noise = 0.0
    r = 0.4
    RB = 1e07
    RBoverLB = 0.0
    rdis = 7000.0
    s1overLG = 0.1
    s1overLB = 1e-04
    s1overCH = (36 * 2.5 * 2 / 25.0) * 1e09


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print "please invoke this script with 2 parameters: (path to the file with beta values over time) and (path to envelope file)"
        quit()

    alphaFile = sys.argv[1]
    envelopeFile = sys.argv[2]
    alphaFileHandle = open(alphaFile, "r")
    envelopeFileHandle = open(envelopeFile, "r")
    outputFile = alphaFile[:-4] + ".song.dat"
    outputFileHandle = open(outputFile, "w")


    def alphaBetaStream():
        betaLine = alphaFileHandle.readline().split()
        if len(betaLine) == 0:
            return (False, False)
        beta = float(betaLine[1])

        envelopeLine = envelopeFileHandle.readline().split()
        alpha = float(envelopeLine[2])

        return (alpha, beta)


    def outStream(line):
        outputFileHandle.write(str(line) + "\n")


    ab2d = AlphaBeta2Dat(alphaBetaStream, outStream)
    ab2d.mainLoop()
