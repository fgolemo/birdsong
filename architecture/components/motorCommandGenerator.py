import math


class MotorCommandGenerator():
    """ Make the raw motor parameters into alpha/beta values over time
    """

    frequency = 10  # number of steps per second

    def __init__(self, frequency):
        self.frequency = frequency

    def getList(self, params):
        """ generate the values in the form of a list, in case that is preferred over a generator
        """
        out = []
        for values in self.getGenerator(params):
            out.append(values)
        return out

    def getGenerator(self, params):
        """ generate the actual pattern over time, return a generator

        general formula:

        alpha = a + b * t + c * sin(d + e*t)
        beta = f + g * t + h * sin(i + j*t)
        for t=[0,k] seconds
        """
        t = 0.0
        while t <= params[10] * self.frequency:
            t_adjusted = t / self.frequency
            alpha = params[0] + \
                    (params[1] * t_adjusted) + \
                    (params[2] * math.sin(params[3] + params[4] * t_adjusted))
            beta = params[5] + \
                   (params[6] * t_adjusted) + \
                   (params[7] * math.sin(params[8] + params[9] * t_adjusted))

            yield (alpha, beta)
            t += 1


if __name__ == "__main__":  # for testing
    mcg = MotorCommandGenerator(frequency=10)
    params = [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 1]

    print "generator:"
    for mc in mcg.getGenerator(params):
        print mc

    print "list:"
    for mc in mcg.getList(params):
        print mc
