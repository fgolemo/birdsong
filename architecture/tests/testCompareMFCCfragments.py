import random
import librosa
import math
import matplotlib.pyplot as plt
from architecture.components.hearing import Hearing
import scipy.stats
import numpy as np


def lookahead(mfcc1, mfcc2, length):
    biases = []
    for i1 in range(length):
        # print mfcc1[:,i1]
        bestMatch = 99999999
        bestMatchIndex = 0
        for i2 in range(length * 2):
            index = i1 + i2 - length
            # print index
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


def compare(mfcc1, mfcc2, bias):
    fits = []
    spanOffset = getSpanOffset(mfcc1)
    for index in range(len(mfcc1[1, :])):
        fitness = compareStep(mfcc1, mfcc2, bias, index, spanOffset)
        # print fitness
        fits.append(fitness)
    averageFit = float(sum(fits)) / len(fits)
    return averageFit


def compareStep(mfcc1, mfcc2, bias, index, spanOffset):
    normSigma = 0  # mean of the normal distribution which punishes differences in timing
    normMu = 1.0  # std. deviation of the normal distribtuion which punishes differences in timing
    normScaling = 1.0 / scipy.stats.norm(normSigma, normMu).pdf(
        0)  # scaling factor so that the probability density at time x=0 is 1
    normWidth = 3  # number of indices to check, right and left of the biased index

    localFits = []
    localFitIndices = range(-normWidth, normWidth + 1)

    for i in localFitIndices:
        if i < 0 or index + bias + i > len(mfcc2[1, :]) - 1:
            localFits.append(0)
            continue

        error = mfcc1[:, index] - mfcc2[:, index + bias + i]
        # print "index",index,"i",i,"bias",bias,"mfcc1",mfcc1[:,index],"mfcc2",mfcc2[:,index + bias + i],"diff",diff
        scaledLocalFitness = calcFitnessFromError(error, spanOffset, i)
        # print "scaled",scaledLocalFitness
        localFits.append(scaledLocalFitness)

    # print "best fit index:",localFitIndices[localFits.index(max(localFits))]
    return max(localFits)

def calcFitnessFromError(error, spanOffset, i):
    normSigma = 0  # mean of the normal distribution which punishes differences in timing
    normMu = 1.0  # std. deviation of the normal distribtuion which punishes differences in timing
    normScaling = 1.0 / scipy.stats.norm(normSigma, normMu).pdf(
        0)  # scaling factor so that the probability density at time x=0 is 1
    normWidth = 3  # number of indices to check, right and left of the biased index

    # print "error",error
    span = spanOffset[0]
    offset = spanOffset[1]
    normalizedError = (error+offset)/(span/2)
    # print "normalizedError",normalizedError
    # squaredNormalizedError = normalizedError**2
    squaredNormalizedError = [abs(e) for e in normalizedError]
    # print "squaredNormalizedError",squaredNormalizedError

    errorSum = sum(squaredNormalizedError)/3
    # print "diffsum:",errorSum

    localFitness = 1-errorSum
    # print "localFitness",localFitness
    if localFitness < 0:
        scaledLocalFitness = 0
    else:
        scaledLocalFitness = localFitness * scipy.stats.norm(normSigma, normMu).pdf(i) * normScaling

    return scaledLocalFitness

def getSpanOffset(mfcc):
    span = max(mfcc.ravel())-min(mfcc.ravel())
    offset = (span/2.0)-max(mfcc.ravel())
    return (span, offset)


testFile1 = "./testSong1Original.wav"
testFile2 = "./testSong2Synth.wav"

h = Hearing(tutorsong=None)
mfcc1 = h.calcMfcc(testFile1)
mfcc2 = h.calcMfcc(testFile2)

mfccZero = np.zeros([3, 22])

mfcc1Range = getSpanOffset(mfcc1)[0]/2
mfccRandom = (np.random.rand(3, 23) * 2 - 1) * mfcc1Range
mfccRandom2 = (np.random.rand(3, 23) * 2 - 1) * mfcc1Range


bias = lookahead(mfcc1, mfcc2, 3)
print "similarity:",compare(mfcc1, mfcc2, bias)

bias = lookahead(mfcc1, mfccZero, 3)
print "similarity:",compare(mfcc1, mfccZero, bias)

bias = lookahead(mfcc1, mfccRandom, 3)
print "similarity:",compare(mfcc1, mfccRandom, bias)

bias = lookahead(mfccRandom, mfccZero, 3)
print "similarity:",compare(mfccRandom, mfccZero, bias)

bias = lookahead(mfccRandom, mfccRandom2, 3)
print "similarity:",compare(mfccRandom, mfccRandom2, bias)


# ax1 = plt.subplot(4, 1, 1)
# librosa.display.specshow(mfcc1, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
#
# plt.subplot(4, 1, 2)
# librosa.display.specshow(mfcc2, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
#
# plt.subplot(4, 1, 3)
# librosa.display.specshow(mfccZero, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
#
# plt.subplot(4, 1, 4)
# librosa.display.specshow(mfccRandom, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
#
# plt.tight_layout()
# plt.show()


