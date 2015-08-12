import os
import cPickle as pickle

__author__ = 'Florian'

dataFolder = "D:/birddata"
outputSongsPerDay = []

print "scanning directory: " + dataFolder
dirContent = os.listdir(dataFolder)
for bird in dirContent:
    birdFolder = dataFolder + os.path.sep + bird
    try:
        if str(int(bird)) != bird or not os.path.isdir(birdFolder):
            continue
    except ValueError:
        continue
    birdContent = os.listdir(birdFolder)
    print "checking bird ", bird
    for day in birdContent:
        dayFolder = birdFolder + os.path.sep + day
        try:
            if str(int(day)) != day or not os.path.isdir(dayFolder):
                continue
        except ValueError:
            continue
        songs = os.listdir(dayFolder)
        for song in songs:
            try:
                nameSegmentsA = song.split(".")
                nameSegmentsB = nameSegmentsA[1].split("_")
                hour = nameSegmentsB[3]
                minute = nameSegmentsB[4]
                second = nameSegmentsB[5]
            except IndexError:
                continue
            outputSongsPerDay.append([bird, day, hour, minute, second, song])

print "directory scan done... writing csv"
with open('todo-cluster.csv', 'w') as outfile:
    for line in outputSongsPerDay:
        outfile.write(",".join(line) + '\n')

print "writing csv done... writing saving pickle"
with open('todo-cluster.pickle', 'wb') as outfile:
    pickle.dump(outputSongsPerDay, outfile)
