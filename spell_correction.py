import numpy as np
from rw_files.create_dawgs import MyDawg
import os
from canditates_generator import generate_candidates

# number of directed acyclic word graphs pickled in dir rw_files/pickles (base_dawg_n.pkl)
NUMBER_OF_DAWGS = 11


class SpellingCorrector:
    """
    Spelling corrector which uses DAWG, and Levenshtein distance
    DONE: 1. change source_of_true implementation from list to DAWG
    DONE: 2. use source_of_true DAWG only for lookup
    DONE: 3. one the word was't found in DAWG then generate all its possible variations (limited by given levenstein)
    DONE: 4. search the source_of_true DAWG for occurrence of the generated words
    http://norvig.com/spell-correct.html?fbclid=IwAR3aoAGLipRXGTEiPvtWAr1mBOPbZdyxbwZ-QCnQx7ZM4KijCm1tqUxa6zk
    """

    def __init__(self, my_dawg=MyDawg()):
        """
        :param my_dawg: instance of MyDawg class for dawg unpickling and all dawg operations
        """
        self.my_dawg = my_dawg
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.filepath = os.path.join(self.abs_path, 'rw_files\\pickles\\')

        # unpickle base dawgs as class members
        b_dawgs_pickle_names = [f"base_dawg_{i + 1}.pkl" for i in range(NUMBER_OF_DAWGS)]
        b_dawgs_pickle_files = list(map(lambda file_name: os.path.join(self.filepath, file_name), b_dawgs_pickle_names))
        self.b_dawgs = [my_dawg.unpickle_dawg(b_dawgs_pickle_file) for b_dawgs_pickle_file in b_dawgs_pickle_files]

        # upickle completion dawgs as class members
        c_dawgs_pickle_names = [f"completion_dawg_{i + 1}.pkl" for i in range(NUMBER_OF_DAWGS)]
        c_dawgs_pickle_files = list(map(lambda file_name: os.path.join(self.filepath, file_name), c_dawgs_pickle_names))
        self.c_dawgs = [my_dawg.unpickle_dawg(c_dawgs_pickle_files) for c_dawgs_pickle_files in c_dawgs_pickle_files]

    def levenshtein(self, seq1, seq2):
        """
        Source: https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
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

    def check_phrase(self, phrase):
        """
        :param phrase: phrase which correctness will be checked
        :return: True if the phrase is in any of DAWGs, otherwise - false
        """
        if True in [self.my_dawg.is_word(b_dawg, phrase) for b_dawg in self.b_dawgs]:
            return True
        else:
            return False

    def correct_phrase(self, phrase, l_distance, search_substution=False, err_type=None):
        """
        :param phrase - string to be checked
        :param l_distance - max levenstein distance between phrase and each word
        :param search_substution - boolean that indicates weather substitutions for correct phrase are needed
        :param err_type TODO use error type as parameter
        """
        is_word = self.check_phrase(phrase)
        if is_word and not search_substution:
            return True, {}
        else:
            candidates = generate_candidates(phrase, l_distance, self.check_phrase)
            return is_word, candidates
        # distances = [self.levenstein(word, phrase) for word in self.source_of_true]
        # words_with_distances = list(zip(self.source_of_true, distances))
        # return sorted(list(filter(lambda wd: wd[1] <= l_distance, words_with_distances)), key=lambda wd: wd[1])


if __name__ == '__main__':
    sg = SpellingCorrector()
    # res = sg.correct_phrase('Kopp', 2)
    res = generate_candidates('Kotp', 3, sg.check_phrase)
    print(res)
