from __future__ import print_function
import os

inPath = "/argile/golemo/birddata-syllables-csv2/"
outPath = "/home/florian.golemo/birddata-csv-1136/"

fileList = "birddata-syllables-csv-list.sorted.txt"
saveFile = "csvCopier.save"

def bufcount(filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines

# with open(fileList) as f:
#     for line in f:

lineCount = bufcount(fileList)

counter = 0

def progress(current, total):
    percentDone = float(current) / total * 100
    tens = int(round(percentDone*2 / 10))
    print("transfer {:.2f}% done, {} out of {} files".format(percentDone,current,total) + " [" + "#" * tens + " " * (20 - tens) + "]",
          end='\r')

lastPos = 0
continueLastPosition = False
if os.path.exists(saveFile):
    with open(saveFile) as f:
        lastPos = int(f.read())
        print("found lastPos: "+str(lastPos))
        continueLastPosition = True

try:
    O_BINARY = os.O_BINARY
except:
    O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
BUFFER_SIZE = 128*1024

def copyfile(src, dst):
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, BUFFER_SIZE), ""):
            os.write(fout, x)
    finally:
        try: os.close(fin)
        except: pass
        try: os.close(fout)
        except: pass

with open(fileList) as f:
    for line in f:
        fileName = line[:-1]
        if continueLastPosition and counter < lastPos:
            counter+=1
            continue
        if line[:4] != "1136":
            counter += 1
            continue
        copyfile(inPath+fileName, outPath+fileName)
        counter += 1
        if counter % 100 == 0:
            sf = open(saveFile, "w")
            sf.write(str(counter))
            sf.close()
            progress(counter, lineCount)

print("DONE!")


