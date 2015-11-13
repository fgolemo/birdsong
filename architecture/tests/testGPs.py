import math

from architecture.components.hearing import Hearing

# cool, mfcc length = (time (in s) * 22050 / 512) + 1

def getMfccLen(audiolength):
    out = math.floor((float(audiolength) * 22050 / 512) + 1)
    return int(out)

# load a bunch of synthed audio files and get the MFCC each

patterns = [
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25],
    [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0.25],
    [0.1, 0.1, 0.1, 0.1, 100, -10, 0.1, 0.1, 0.1, 100, 0.25],
    [10, 10, 10, 10, 10, -10, 10, 10, 10, 10, 0.25],
    [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 0.25],
    [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, -0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.25]
]

testfiles = [
    "./testpattern-0.wav",
    "./testpattern-2.wav",
    "./testpattern-3.wav",
    "./testpattern-4.wav",
    "./testpattern-6.wav",
    "./testpattern-7.wav"
]

h = Hearing(tutorsong=None)
mfccs = []

for tf in testfiles:
    mfcc = h.calcMfcc(tf)
    mfccs.append(mfcc)

# for mfcc in mfccs:
#     print mfcc.shape

trainingDataInput = []
trainingDataOutput = []

for patternIndex in range(len(patterns)):
    mfccLen = getMfccLen(patterns[patternIndex][-1])
    for i in range(mfccLen):
        patternWithTimestamp = [i]+patterns[patternIndex]
        trainingDataInput.append(patternWithTimestamp)
        trainingDataOutput.append(mfccs[patternIndex][:,i])

import numpy as np
from sklearn import gaussian_process

X = np.atleast_2d(trainingDataInput)
y = np.atleast_2d(trainingDataOutput)

print X.shape
print y.shape

gp = gaussian_process.GaussianProcess(theta0=1e-2, regr="quadratic")
print "created model, now fitting"
gp.fit(X, y)
print "fitted model, now predicting"
tests = np.atleast_2d([
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 0],
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 1],
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 2],
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 8],
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 9],
    [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 10],
    [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 0],
    [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 1],
    [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 2],
    [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 8],
    [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 9],
    [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 10]
]).T

y_pred, sigma2_pred = gp.predict(tests, eval_MSE=True)

print y_pred
print sigma2_pred



