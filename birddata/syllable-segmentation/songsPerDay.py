import os

__author__ = 'Florian'

""" Scan all the bird folders and create a CSV file with how often they sang every hour, counted by the number of files.
"""

if __name__ == "__main__":
    initialFolder = "E:"
    outputSongsPerDay = []
    outputSongsPerHourTemplate = dict(zip(range(0, 24), [0 for x in range(0, 24)]))

    dirContent = os.listdir(initialFolder)
    for bird in dirContent:
        birdFolder = initialFolder + os.path.sep + bird
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
            outputSongsPerHour = dict(zip(range(0, 24), [0 for x in range(0, 24)]))
            for song in songs:
                try:
                    nameSegmentsA = song.split(".")
                    nameSegmentsB = nameSegmentsA[1].split("_")
                    hour = nameSegmentsB[3]
                except IndexError:
                    continue
                outputSongsPerHour[int(hour)] += 1
            outputSongsPerHourList = [str(val) for key, val in outputSongsPerHour.iteritems()]
            outputSongsPerDay.append([bird, day, str(len(songs))] + outputSongsPerHourList)

    with open('songsPerDay.csv', 'w') as outfile:
        for line in outputSongsPerDay:
            outfile.write(",".join(line) + '\n')
