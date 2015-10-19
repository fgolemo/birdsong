import math


class AlphaBeta2Dat():
    def __init__(self, alphaFile, envelopeFile):
        self.numberOfLines = sum(1 for line in open(alphaFile))
        self.outputFile = alphaFile[:-4] + ".song.dat"

        self.alphaFileHandle = open(alphaFile, "r")
        self.envelopeFileHandle = open(envelopeFile, "r")
        self.outputFileHandle = open(self.outputFile, "w")

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
        self.to = self.numberOfLines * self.stepping
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

        self.a = [0] * int(self.to)
        self.bf = [0] * int(self.to)
        self.bb = [0] * int(self.to)
        self.cf = [0] * int(self.to)
        self.cb = [0] * int(self.to)
        self.df = [0] * int(self.to)
        self.db = [0] * int(self.to)

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
        while self.t < self.to and self.v[1] > -5000000:
            self.dbold = self.db[self.t]

            self.a[self.t] = 0.5 * (1.01 * (1.0 * (self.birdstate.A1 * self.v[1] +
                                                   self.birdstate.A2 * self.v[6] +
                                                   self.birdstate.A3 * self.v[9] / 10.))) + \
                             self.bb[self.t - self.tau1]
            self.bb[self.t] = self.r12 * self.a[self.t - self.tau1] + \
                              self.t21 * self.cb[self.t - self.tau2]
            self.bf[self.t] = self.t12 * self.a[self.t - self.tau1] + \
                              self.r21 * self.cb[self.t - self.tau2]

            self.cb[self.t] = self.r23 * self.bf[self.t - self.tau2] + \
                              self.t32 * self.db[self.t - self.tau3]
            self.cf[self.t] = self.t23 * self.bf[self.t - self.tau2] + \
                              self.r32 * self.db[self.t - self.tau3]
            self.db[self.t] = -self.birdstate.r * self.cf[self.t - self.tau3]

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
                betaLine = self.alphaFileHandle.readline().split()
                self.birdstate.beta1 = float(betaLine[1])

                envelopeLine = self.envelopeFileHandle.readline().split()
                self.birdstate.amplitud = float(envelopeLine[2])

                self.outputFileHandle.write(str(self.preout * 10) + "\n")

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

    ab2d = AlphaBeta2Dat(alphaFile=sys.argv[1], envelopeFile=sys.argv[2])
    ab2d.mainLoop()
