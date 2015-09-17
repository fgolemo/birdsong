from __future__ import print_function
import shutil
import os
import sys

filepath = "E:\\birddata-wav"
outpath = "E:\\birddata-flac"
if len(sys.argv) == 3:
    filepath = os.path.abspath(os.path.expanduser(sys.argv[1]))
    outpath = os.path.abspath(os.path.expanduser(sys.argv[2]))

matches = []
print("scanning directories for FLAC files")

dirsToMake = []
copyFiles = []

print("creating index of files to copy")
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
print("indexing done")

print("making directories")
for directory in dirsToMake:
    if not os.path.isdir(outpath + directory):
        os.makedirs(outpath + directory)
print("making directories done")

i = 0
print("transferring files")
for copyFile in copyFiles:
    src = filepath + os.sep + copyFile[0] + os.sep + copyFile[1] + os.sep + copyFile[2]
    dest = outpath + os.sep + copyFile[0] + os.sep + copyFile[1] + os.sep + copyFile[2]
    i += 1
    percentDone = float(i) / len(copyFiles) * 100
    print("{:.2f}% done".format(percentDone), end='\r')
    if os.path.exists(dest) and os.path.getsize(dest) == os.path.getsize(src):
        continue
    else:
        if os.path.exists(dest) and os.path.getsize(dest) != os.path.getsize(src):
            os.remove(dest)
    shutil.copy2(src, dest)


print("\ntransferring files done")
