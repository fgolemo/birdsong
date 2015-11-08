
class Comparator:
    def __init__(self, strategy):
        """ Initialize the class: store the strategy

        :param strategy: String, currently either "seq" or "sim" for "sequential" and "simultaneous" respectively
        :return: None
        """
        self.strategy = strategy

    def calcDiff(self, tutorMfcc, songMfccList, isDayTime):
        """ calculate the fitness of a given song, compared to the tutorsong,
        while paying attention to the strategy and the day/night cycle

        :param tutorMfcc: matrix with width 3 over time (representing the first 3 MFCC features of the tutor song over time)
        :param songMfccList:  list of matrices, where each matrix is a syllable in the same format as tutorMFCC
        :param isDayTime: boolean switch to indicate if it's daytime (False = nighttime)
        :return: list of normalized fitness values for each syllable
        """

        pass





