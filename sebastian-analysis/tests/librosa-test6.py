# We'll need numpy for some mathematical operations
import numpy as np

# Librosa for audio
import librosa

# matplotlib for displaying the output
import matplotlib.pyplot as plt
# %matplotlib inline
# And seaborn to make it look nice
import seaborn
seaborn.set(style='ticks')

from scipy import fft, ifft
from scikits.audiolab import flacread


amp_threshold = 1.0e-09  # if the amp of any freq is higher than this, it will be counted as good
freq_threshold = 5  # if the number of good freqs (see prev line) is higher than this, it's probably birdsong
smoothing = 15  # HAS TO BE >1, also keep the bins N to the left and right of good segments

zero_val = 1.23e-12

# audio_path = "../b1136.d94.t282148.flac"
# audio_path = "../b1592.d54.t66047281.flac"
audio_path = "../amp-test.flac"
y, sr = librosa.load(audio_path)
print 'HAS_SAMPLERATE: ', librosa.core.audio._HAS_SAMPLERATE


plt.figure(figsize=(12, 10))

data, sample_freq, encoding = flacread(audio_path)

timeArray = np.arange(0.0, len(data), 1)
timeArray = timeArray / sample_freq
timeArray = timeArray * 1000  # scale to milliseconds

NFFT = 1000  # the length of the windowing segments

fft = fft(data)  # FFT
bp = fft[:]  # copy for manipulating //currently not needed
ibp = ifft(bp)  # inverse FFT for spectrogram

ax1 = plt.subplot(6, 1, 1)
plt.plot(timeArray, data)
plt.subplot(6, 1, 2)
Pxx, freqs, bins, im = plt.specgram(data, Fs=sample_freq)


def loudBits(slice):
    return [1 if slice[i] > amp_threshold else 0 for i in range(len(slice))]


dataMod = data[:]

goodSegmentCount = 0

i = 0
prevGood = False
while i < len(bins):
    step = 1
    goodSegmentsInThere = False
    for j in range(smoothing):
        if i + j == len(bins):
            break
        lb = loudBits(Pxx[:, i + j])
        if sum(lb) > freq_threshold:
            goodSegmentsInThere = True
            step = j + 1
            prevGood = True
            break
    if not goodSegmentsInThere:
        if prevGood:
            step = smoothing - 1
        else:
            for k in range(128):
                dataMod[i * 128 + k] = zero_val
        prevGood = False
    i += step

plt.subplot(6, 1, 3)
plt.plot(timeArray, dataMod)
plt.subplot(6, 1, 4)
Pxx2, freqs2, bins2, im2 = plt.specgram(dataMod, Fs=sample_freq)

S = librosa.feature.melspectrogram(dataMod, sr=sr, n_mels=10)
log_S = librosa.logamplitude(S, ref_power=np.max)


mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=3)
mfcc2 = mfcc[1:3, :]
delta_mfcc = librosa.feature.delta(mfcc)
plt.subplot(6, 1, 5)
librosa.display.specshow(mfcc)
plt.ylabel('MFCC')
# plt.colorbar()

plt.subplot(6, 1, 6)
librosa.display.specshow(delta_mfcc)
plt.ylabel('MFCC-$\Delta$')
# plt.colorbar()

plt.tight_layout()


plt.show()
