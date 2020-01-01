import numpy as np


class SpellGuard:
    """
    This is a naive implementation of this class - it uses brute force lookup and stores correct words as a list
    :param source_of_true list of correct words in our language
    TODO: 1. change source_of_true implementation from list to DAWG
    TODO: 2. use source_of_true DAWG only for lookup
    DONE: 3. one the word was't found in DAWG then generate all its possible variations (limited by given levenstein)
    TODO: 4. search the source_of_true DAWG for occurrence of the generated words
    http://norvig.com/spell-correct.html?fbclid=IwAR3aoAGLipRXGTEiPvtWAr1mBOPbZdyxbwZ-QCnQx7ZM4KijCm1tqUxa6zk
    """

    def __init__(self, source_of_true):
        self.source_of_true = source_of_true

    def levenstein(self, seq1, seq2):
        """
        Source:
        https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
        :param seq1 string
        :param seq2 string
        :returns leventein distance between seq1 and seq2 (number)
        """
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y

        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x - 1] == seq2[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                    )
        # print(matrix)
        return matrix[size_x - 1, size_y - 1]

    def spell_check(self, phrase, l_distance, err_type=None):
        """
        Calculates Levenstein distance between phrase and each word from source of true
        :param phrase - string to be checked
        :param l_distance - max levenstein distance between phrase and each word
        :param err_type TODO use error type as parameter
        """
        distances = [self.levenstein(word, phrase) for word in self.source_of_true]
        words_with_distances = list(zip(self.source_of_true, distances))
        return sorted(list(filter(lambda wd: wd[1] <= l_distance, words_with_distances)), key=lambda wd: wd[1])

    def set_source_of_true_from_file(self, file):
        """
        Sets the source of true (list of correct words) to match content of given file
        :param file - file containing all correct word
        """
        self.source_of_true = []
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if ',' in line:
                    words = line.replace(' ', '').split(',')
                    self.source_of_true.extend(words)
                else:
                    self.source_of_true.extend(line)


sg = SpellGuard(['Hanna', 'Anna', 'Nanana', 'nanana', 'na'])
sg.set_source_of_true_from_file('slownik_mini.txt')
print(sg.spell_check('panna', 3, None))
