import librosa
import math
import matplotlib.pyplot as plt
from architecture.components.hearing import Hearing


testFile1 = "./testSong1Original.wav"
testFile2 = "./testSong2Synth.wav"

h = Hearing(tutorsong=None)
mfcc1 = h.calcMfcc(testFile1)
mfcc2 = h.calcMfcc(testFile2)

# ax1 = plt.subplot(2, 1, 1)
# librosa.display.specshow(mfcc1, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
# plt.subplot(2, 1, 2)
# librosa.display.specshow(mfcc2, x_axis='time')
# plt.colorbar()
# plt.title('MFCC')
# plt.tight_layout()
# plt.show()


def lookahead(mfcc1, mfcc2, length):
    biases = []
    for i1 in range(length):
        # print mfcc1[:,i1]
        bestMatch = 99999999
        bestMatchIndex = 0
        for i2 in range(length*2):
            index = i1+i2-length
            print index
            if index < 0:
                continue
            if index > len(mfcc2)-1:
                break
            diff = mfcc1[:,i1]-mfcc2[:,index]
            diffScalar = sum([abs(element) for element in diff])
            if diffScalar < bestMatch:
                bestMatch = diffScalar
                bestMatchIndex = index
        bias = bestMatchIndex
        biases.append(bias)

    # return rounded averaage
    #return int(round(float(sum(biases))/len(biases),0))

    # return mode (better)
    return max(set(biases), key=biases.count)

print lookahead(mfcc1,mfcc2, 3)




