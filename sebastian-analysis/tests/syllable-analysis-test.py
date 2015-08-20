from __future__ import division
from pylab import *
from scipy.io import wavfile
from scipy import fft, ifft

__author__ = 'Florian'

from scikits.audiolab import wavread, available_encodings, available_file_formats, Sndfile
import numpy as np

for format in available_file_formats():
    print "File format %s is supported; available encodings are:" % format
    for enc in available_encodings(format):
        print "\t%s" % enc
    print ""
quit()

data, sample_freq, encoding = wavread('b1136.d94.t282148.wav')
print sample_freq
print encoding
print type(data)
print data.shape
print data[0:10]
print len(data)
print min(data)
print max(data)

print len(data) / sample_freq  # song length in s

timeArray = arange(0.0, len(data), 1)
timeArray = timeArray / sample_freq
timeArray = timeArray * 1000  # scale to milliseconds


# plot(timeArray, data, color='k')
# ylabel('Amplitude')
# xlabel('Time (ms)')
# show()

NFFT = 1000  # the length of the windowing segments

fft = fft(data)  # (G) and (H)
bp = fft[:]
print bp[1:50]
print "len bp:", len(bp)
# for i in range(len(bp)):  # (H-red)
#     if i >= 650:
#         bp[i] = 0
print bp[1:50]

ibp = ifft(bp)  # (I), (J), (K) and (L)

ax1 = subplot(4, 1, 1)
plot(timeArray, data)
subplot(4, 1, 2)
Pxx, freqs, bins, im = specgram(data, Fs=sample_freq)
subplot(4, 1, 3)
plot(timeArray, ibp)
subplot(4, 1, 4)
Pxx2, freqs2, bins2, im2 = specgram(ibp, Fs=sample_freq)

matchA = False
matchB = False
# matchB = False
print "bins", len(bins), bins.shape
print "freqs", len(freqs), freqs.shape
print "Pxx", len(Pxx), Pxx.shape
for i in range(len(bins)):
    if bins[i] > 2.10484 and not matchA:
        # print 1
        # print i
        # print freqs[i]
        # print Pxx[:,i]
        a = Pxx[:, i]
        matchA = True
    if bins[i] > 2.124 and not matchB:
        # print 3
        # print freqs[i]
        # print i
        # print Pxx[:,i]
        b = Pxx[:, i]
        matchB = True
        # break
    if bins[i] > 2.16129:
        # print 3
        # print freqs[i]
        # print i
        # print Pxx[:,i]
        # b=Pxx[:,i]
        c = Pxx[:, i]
        break


def loudBits(slice):
    return [1 if slice[i] > 1e-09 else 0 for i in range(len(slice))]


print sum(loudBits(a))
print sum(loudBits(b))
print sum(loudBits(c))

# print Pxx[0:20]
# print freqs[0:20]
# print bins[0:20]
# print type(im)
# print max(bins)
# show()
