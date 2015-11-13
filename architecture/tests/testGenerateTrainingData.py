import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentparentdir)

import os
import random
import sys
from architecture.components.hearing import Hearing
from architecture.components.motorCommandGenerator import MotorCommandGenerator
from architecture.components.soundSynthesizer import SoundSynthesizer
from architecture.synth.dat2wav import Dat2Wav

if __name__ == "__main__":

    numberOfSamples = 100
    if len(sys.argv) >= 2:
        numberOfSamples = int(sys.argv[1])

    outFileNamePrefix = "fmmTrainingData"
    if len(sys.argv) >= 3:
        outFileNamePrefix = sys.argv[2]

    filehandleInputs = open(outFileNamePrefix + ".inputs.csv", "w")
    filehandleOutputs = open(outFileNamePrefix + ".outputs.csv", "w")
    filehandleTemp = outFileNamePrefix + ".tmp.wav"


    def r(scaling):
        return random.random() * scaling - (scaling / 2)


    for i in range(numberOfSamples):
        spans = [
            # random number spans (random number between e.g. -0.01 and +0.01, using the r(scaling) function above
            0.01,
            0.1,
            1,
            2,
            4,
            8,
            16,
            32,
            64,
            100
        ]
        durations = [
            0.25,
            0.5,
            0.75,
            1
        ]
        s = random.choice(spans)
        d = random.choice(durations)

        # pick 10 random variables between -span (s) and span (s) with duration d
        pattern = [r(s), r(s), r(s), r(s), r(s), r(s), r(s), r(s), r(s), r(s), d]

        mcg = MotorCommandGenerator(frequency=44100)
        print "start synthing pattern (", i, ") ", pattern
        alphaBetaList = mcg.getList(pattern)
        j = 0


        def inputStream():
            global j
            if j < len(alphaBetaList):
                j += 1
                return alphaBetaList[j - 1]
            else:
                return (False, False)


        output = []


        def outputStream(content):
            global output
            output.append(content)


        ss = SoundSynthesizer(inputStream, outputStream)
        ss.synthesize()

        d2w = Dat2Wav
        sound = d2w.convert(output)
        d2w.writeWAV(sound, filehandleTemp, 44100)

        print "done synthing, now creating data"

        h = Hearing(tutorsong=None)
        mfcc = h.calcMfcc(filehandleTemp)

        for mfccIndex in range(len(mfcc[1, :])):

            patternStr = [str(p) for p in pattern]
            filehandleInputs.write(",".join([str(mfccIndex)] + patternStr) + "\n")

            mfccStr = [str(m) for m in mfcc[:, mfccIndex]]
            filehandleOutputs.write(",".join(mfccStr) + "\n")

        os.remove(filehandleTemp)

        print "done writing data\n"

    filehandleInputs.close()
    filehandleOutputs.close()
