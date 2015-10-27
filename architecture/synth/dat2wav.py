import sys
import wave
import struct


class Dat2Wav():
    @staticmethod
    def convert(inputList):

        inputListFloat = [float(line) for line in inputList]
        ampMax = max(inputListFloat)
        ampMin = min(inputListFloat)

        sound = []

        if ampMax - ampMin == 0:
            scalingFactor = 1
        else:
            scalingFactor = 65535.0 / (ampMax - ampMin)
        for line in inputListFloat:
            amp = int(round(((line - ampMin) * scalingFactor) - 32768.0))

            if amp > 32767:
                amp = 32767
            if amp < -32768:
                amp = -32768

            sound.append(amp)

        return sound

    @staticmethod
    def writeWAV(sound, outputfile, samplerate):
        outputHandle = open(outputfile, "wb")
        data_as_bytes = (struct.pack('h', i) for i in sound)
        wavwriter = wave.open(outputHandle)
        wavwriter.setnchannels(1)
        wavwriter.setsampwidth(2)
        wavwriter.setframerate(samplerate)
        for data_bytes in data_as_bytes:
            wavwriter.writeframes(data_bytes[0:2])
        wavwriter.close()


if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print "Usage: python dat2wav.py INPUTFILE OUTPUTFILE [SAMPLERATE=44100]"
        exit()

    samplerate = 44100
    if len(sys.argv) == 4:
        samplerate = int(sys.argv[3])
    d2w = Dat2Wav()
    inputFileHandle = open(sys.argv[1], "r")
    inputList = inputFileHandle.readlines()
    sound = d2w.convert(inputList)
    d2w.writeWAV(sound, sys.argv[2], samplerate)
