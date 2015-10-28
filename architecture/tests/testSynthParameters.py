import random
from architecture.components.motorCommandGenerator import MotorCommandGenerator
from architecture.components.soundSynthesizer import SoundSynthesizer
from architecture.synth.dat2wav import Dat2Wav

if __name__ == "__main__":

    def r(scaling):
        return random.random() * scaling - (scaling / 2)


    patterns = [
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.25],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0.25],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25],
        [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0.25],
        [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, 0.25],
        [1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 0.25],
        [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.25],
        [r(2), r(2), r(2), r(2), r(2), r(2), r(2), r(2), r(2), r(2), 0.25],
        [r(4), r(4), r(4), r(4), r(4), r(4), r(4), r(4), r(4), r(4), 0.25],
        [r(10), r(10), r(10), r(10), r(10), r(10), r(10), r(10), r(10), r(10), 0.25]
    ]

    mcg = MotorCommandGenerator(frequency=44100)

    for j in range(len(patterns)):

        print "start synthing pattern " + str(j)
        alphaBetaList = mcg.getList(patterns[j])
        i = 0


        def inputStream():
            global i
            if i < len(alphaBetaList):
                i += 1
                return alphaBetaList[i - 1]
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
        d2w.writeWAV(sound, "testpattern-" + str(j) + ".wav", 44100)

        print "done synthing pattern " + str(j)
