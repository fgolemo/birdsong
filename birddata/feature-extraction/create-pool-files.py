import sys
import os


if __name__ == "__main__":
    defaultPath = "/home/florian.golemo/syllable-file-list.txt"

    pathToLookForOutput = "/argile/golemo/birddata-syllables-csv/"

    if len(sys.argv) < 2:
        print "need one (optional) argument: path to the file that has a list with all the syllable files"
        print "assuming: ",defaultPath
        filePath = defaultPath
    else:
        if os.path.isfile(sys.argv[1]):
            filePath = sys.argv[1]
        else:
            print "supplied argument is not a file:",sys.argv[1]
            quit()

    with open(filePath) as infile, open(filePath+".leftOver") as outfile:
        for line in infile:
            if not os.path.isfile(line + ".csv"):
                outfile.write(line)




