from __future__ import print_function
import fnmatch
import os
import sys
import pysox

filepath = "/media/florian/My Passport/1136"
if len(sys.argv) == 2:
    filepath = os.path.abspath(os.path.expanduser(sys.argv[1]))

matches = []
print("scanning directories for WAV files")
for root, dirnames, filenames in os.walk(filepath):
    for filename in fnmatch.filter(filenames, '*.wav'):
        matches.append(os.path.join(root, filename))
nMatches = len(matches)
print("scanning done, found " + str(len(matches)) + " files")

print("converting now")
counter = 0
for match in matches:
    outName = match[:-3]+"flac"
    counter += 1
    percentDone = float(counter) / nMatches * 100
    print("{:.2f}% done".format(percentDone), end='\r')
    if os.path.isfile(outName):
        continue
    try:
        app = pysox.CSoxApp(match, outName)
        app.flow()
    except IOError:
        print ("\nIOError at file: "+match+". Skipping")

print("\nconversion done")

