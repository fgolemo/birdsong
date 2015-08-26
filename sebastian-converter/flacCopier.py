from __future__ import print_function
import fnmatch
import os
import sys

filepath = "D:/birddata"
outpath = "D:/birddata2"
if len(sys.argv) == 3:
    filepath = os.path.abspath(os.path.expanduser(sys.argv[1]))

matches = []
print("scanning directories for FLAC files")

dirsToMake = []
copyFiles = []

birds = os.listdir(filepath)
for bird in birds:
    birdpath = filepath + os.path.sep + bird
    if not os.path.isdir(birdpath):
        continue
    dirsToMake.append(os.path.sep + bird)
    days = os.listdir(birdpath)
    for day in days:
        daypath = birdpath + os.path.sep + day
        if not os.path.isdir(daypath):
            continue
        dirsToMake.append(os.path.sep + bird + os.sep + day)
        songs = os.listdir(daypath)
        for song in songs:
            if song[-4:] == "flac":
                copyFiles.append([bird, day, song])

for directory in dirsToMake:
    os.makedirs(outpath + directory, exist_ok=True)

for copyFile in copyFiles:

    pass

