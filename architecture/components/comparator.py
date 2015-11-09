import scipy.stats


class Comparator:
    def __init__(self, strategy):
        """ Initialize the class: store the strategy

        :param strategy: String, currently either "seq" or "sim" for "sequential" and "simultaneous" respectively
        :return: None
        """
        if strategy not in ["seq", "sim"]:
            raise AttributeError("please initialize the comparater with the strategy "
                                 "parameter being either 'seq' or 'sim'. You provided: '" + str(strategy) + "'")
        self.strategy = strategy

        self.normSigma = 0  # mean of the normal distribution which punishes differences in timing
        self.normMu = 1.0  # std. deviation of the normal distribtuion which punishes differences in timing
        # scaling factor so that the probability density at time x=0 is 1
        self.normScaling = 1.0 / scipy.stats.norm(self.normSigma, self.normMu).pdf(0)
        self.normWidth = 3  # number of indices to check, right and left of the biased index
        self.biasLookahead = 3  # dynamic time shift width (+/- N timesteps / MFCC buckets)

    def calcDiff(self, tutorMfcc, songMfccList, isDayTime):
        """ calculate the fitness of a given song, compared to the tutorsong,
        while paying attention to the strategy and the day/night cycle

        :param tutorMfcc: matrix with width 3 over time (representing the first 3 MFCC features of the tutor song over time)
        :param songMfccList:  list of matrices, where each matrix is a syllable in the same format as tutorMFCC
        :param isDayTime: boolean switch to indicate if it's daytime (False = nighttime)
        :return: list of normalized fitness values for each syllable
        """

        lastTutorIndex = 0
        fits = []

        for syllableMfcc in songMfccList:
            syllableMfccLen = len(syllableMfcc)
            if lastTutorIndex + syllableMfccLen > len(tutorMfcc):
                fits.append(0)
                continue
            tutorMfccInterval = tutorMfcc[:, lastTutorIndex:syllableMfccLen]
            fragmentBias = self.lookahead(tutorMfccInterval, syllableMfcc, self.biasLookahead)
            fit = self.compareSyllable(tutorMfccInterval, syllableMfcc, fragmentBias)
            fits.append(fit)
            lastTutorIndex += syllableMfccLen

        return fits

    def lookahead(self, mfcc1, mfcc2, length):
        biases = []
        for i1 in range(length):
            bestMatch = 99999999
            bestMatchIndex = 0
            for i2 in range(length * 2):
                index = i1 + i2 - length
                if index < 0:
                    continue
                if index > len(mfcc2) - 1:
                    break
                diff = mfcc1[:, i1] - mfcc2[:, index]
                diffScalar = sum([abs(element) for element in diff])
                if diffScalar < bestMatch:
                    bestMatch = diffScalar
                    bestMatchIndex = index
            bias = bestMatchIndex
            biases.append(bias)

        # return rounded averaage
        # return int(round(float(sum(biases))/len(biases),0))

        # return mode (better)
        return max(set(biases), key=biases.count)

    def compareSyllable(self, mfcc1, mfcc2, bias):
        fits = []
        spanOffset = self.getSpanOffset(mfcc1)
        for index in range(len(mfcc1[1, :])):
            fitness = self.compareStep(mfcc1, mfcc2, bias, index, spanOffset)
            # print fitness
            fits.append(fitness)
        averageFit = float(sum(fits)) / len(fits)
        return averageFit

    def compareStep(self, mfcc1, mfcc2, bias, index, spanOffset):
        localFits = []
        localFitIndices = range(-self.normWidth, self.normWidth + 1)

        for i in localFitIndices:
            if i < 0 or index + bias + i > len(mfcc2[1, :]) - 1:
                localFits.append(0)
                continue

            error = mfcc1[:, index] - mfcc2[:, index + bias + i]
            scaledLocalFitness = self.calcFitnessFromError(error, spanOffset, i)
            localFits.append(scaledLocalFitness)

        return max(localFits)

    def calcFitnessFromError(self, error, spanOffset, i):
        span = spanOffset[0]
        offset = spanOffset[1]
        normalizedError = (error + offset) / (span / 2)
        absNormalizedError = [abs(e) for e in normalizedError]

        errorSum = sum(absNormalizedError) / 3

        localFitness = 1 - errorSum
        if localFitness < 0:
            scaledLocalFitness = 0
        else:
            scaledLocalFitness = localFitness * scipy.stats.norm(self.normSigma, self.normMu).pdf(i) * self.normScaling

        return scaledLocalFitness

    def getSpanOffset(self, mfcc):
        span = max(mfcc.ravel()) - min(mfcc.ravel())
        offset = (span / 2.0) - max(mfcc.ravel())
        return (span, offset)


if __name__ == "__main__":
    # TODO: implement tests
    pass
