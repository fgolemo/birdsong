from architecture.components.hearing import Hearing

testFile1 = "./mfccLengthTest1s.wav"
testFile2 = "./mfccLengthTest2s.wav"
testFile05 = "./mfccLengthTest05s.wav"
testFile2505 = "./mfccLengthTest25s5.wav"

h = Hearing(tutorsong=None)
mfcc1 = h.calcMfcc(testFile1)
mfcc2 = h.calcMfcc(testFile2)
mfcc3 = h.calcMfcc(testFile05)
mfcc4 = h.calcMfcc(testFile2505)

print mfcc1.shape
print mfcc2.shape
print mfcc3.shape
print mfcc4.shape

# cool, mfcc length = (time (in s) * 22050 / 512) + 1



