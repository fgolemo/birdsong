#!/usr/bin/env python
import io
from wavebender import *
import sys
import winsound
from cStringIO import StringIO
from wavebender import *
from itertools import *
import sys


# def violin(amplitude=0.1):
#     # simulates a violin playing G.
#     return (damped_wave(400.0, amplitude=0.76*amplitude, length=44100 * 5),
#             damped_wave(800.0, amplitude=0.44*amplitude, length=44100 * 5),
#             damped_wave(1200.0, amplitude=0.32*amplitude, length=44100 * 5),
#             damped_wave(3400.0, amplitude=0.16*amplitude, length=44100 * 5),
#             damped_wave(600.0, amplitude=1.0*amplitude, length=44100 * 5),
#             damped_wave(1000.0, amplitude=0.44*amplitude, length=44100 * 5),
#             damped_wave(1600.0, amplitude=0.32*amplitude, length=44100 * 5)
#             )
# channels = (violin(),)
# samples = compute_samples(channels, 44100 * 60 * 1)


# noise = cycle(islice(white_noise(amplitude=0.006), 44100))
# channels = ((sine_wave(300.0, amplitude=0.1), sine_wave(100.0, amplitude=0.1), sine_wave(500.0, amplitude=0.1), noise),
#             (sine_wave(304.0, amplitude=0.1), sine_wave(100.0, amplitude=0.1), sine_wave(500.0, amplitude=0.1), noise))
# samples = compute_samples(channels,  44100 * 3)


channels = ((sine_wave(140.0, amplitude=0.1),), (sine_wave(440.0, amplitude=0.1),))
samples = compute_samples(channels, 44100 * 2)

outputBuf = io.BytesIO()
write_wavefile(outputBuf, samples, 44100 * 2, nchannels=2)
print "done capturing, starting playback"
winsound.PlaySound(outputBuf.getvalue(), winsound.SND_MEMORY)

# filename = open("soundtext.wav", 'wb')
# write_wavefile(filename, samples, 44100 * 2, nchannels=1)
