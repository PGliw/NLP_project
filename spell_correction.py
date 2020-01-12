import numpy as np
from rw_files.create_dawgs import MyDawg
import os
from canditates_generator import generate_candidates
from distance_calculation import damerau_levenshtein_distance as dl_dist, levenshtein_distance as l_dist

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


    def check_phrase(self, phrase):
        """
        :param phrase: phrase which correctness will be checked
        :return: True if the phrase is in any of DAWGs, otherwise - false
        """
        if True in [self.my_dawg.is_word(b_dawg, phrase) for b_dawg in self.b_dawgs]:
            return True
        else:
            return False

    def correct_phrase(self, phrase, l_distance, search_substitution=False, err_type=None):
        """
        :param phrase - string to be checked
        :param l_distance - max levenstein distance between phrase and each word
        :param search_substitution - boolean that indicates weather substitutions for correct phrase are needed
        :param err_type TODO use error type as parameter
        """
        is_word = self.check_phrase(phrase)
        if is_word and not search_substitution:
            return True, {}
        else:
            candidates = generate_candidates(phrase, l_distance, self.check_phrase)
            candidates_with_distances = [(cand, l_dist(cand, phrase)) for cand in candidates]
            return is_word, sorted(candidates_with_distances, key=lambda tup: tup[1])
        # distances = [self.levenstein(word, phrase) for word in self.source_of_true]
        # words_with_distances = list(zip(self.source_of_true, distances))
        # return sorted(list(filter(lambda wd: wd[1] <= l_distance, words_with_distances)), key=lambda wd: wd[1])


if __name__ == '__main__':
    sc = SpellingCorrector()
    # res = sg.correct_phrase('Kopp', 2)
    res = sc.correct_phrase('Kot', 2, True)
    print(res)
