import random
import sys
import math

__author__ = 'Florian'

# filename = sys.argv[1]
filename = "linear1m1s.test.txt"

incache = []  # file with stream of motor and sensor signals
output = []  # set of caus & effect rules
# genotype = [] # set of sequence associations tuples
rules = []

punishment = {
    "lenSensError": 1,
    "lenMotoError": 1,
    "effectError": 5,
}
maxInitSegLen = 3
replayMemoryPercent = 50  # in percent integer
iterations = 10


def cacheInput():
    with open(filename) as f:
        for line in f:
            digits = line[:-1].split(" ")
            incache.append(digits)


def randomInit():
    i = 0
    while i < len(incache):
        segLen = random.randint(1, maxInitSegLen)
        if i + segLen > len(incache):
            segLen = len(incache) - i
        rule = incache[i:i + segLen]
        i += segLen
        rules.append(rule)


def main():
    # LOOP
    #   select random memory segments
    #       in each memory segment, see if rules are applicable
    #       if rules are applicable, rate their quality
    #   select the fittest rules
    #   crossover the fittest rules
    #   mutate
    # END
    for iteration in range(iterations):
        memSegments = selectRandomMemorySegments()
        for memSegment in memSegments:
            applicableRules = findApplicableRules(memSegment)


def selectRandomMemorySegments():
    indices = range(len(incache))
    random.shuffle(indices)
    maxLen = int(math.ceil(len(incache) * replayMemoryPercent / 100))
    indices = indices[0:maxLen]
    indices.sort()
    i = 0
    out = []
    start = indices[0]
    while i < len(indices):
        cut = False
        done = False
        if i + 1 == len(indices):
            cut = True
            done = True
        else:
            if indices[i + 1] != indices[i] + 1:
                cut = True

        if cut:
            out.append((start, indices[i] + 1))
            if not done:
                start = indices[i + 1]

        i += 1
    return out


def findApplicableRules(memSegment):
    # TODO
    pass
