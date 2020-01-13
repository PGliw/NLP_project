import time

class WordGenerator:
    def __init__(self,
                 correct_word_predicate=None,
                 alphabet='aąbcćdeęfghijklmnoópqrsśtuvwxyzźż',
                 is_deleting=True, is_transposing=True,
                 is_replacing=True, is_inserting=True):
        # inicjalizacjia atrybutów
        """
        :param correct_word_predicate: function (word) -> Boolean. If None than all words are correct.
        :param alphabet: alphabet used to generate strings from given word
        :param is_splitting tells whether to use split operations during generation
        :param is_deleting tells whether to use split operations during generation
        :param is_transposing tells whether to use transpose operations during generation
        :param is_replacing tells whether to use replace operations during generation
        :param is_inserting tells weather to use insert operations during generation
        """
        self.correct_word_predicate = correct_word_predicate
        self.alphabet = alphabet
        self.is_deleting = is_deleting
        self.is_transposing = is_transposing
        self.is_replacing = is_replacing
        self.is_inserting = is_inserting

    def generate_candidates(self, word, max_dist):
        # generowanie możliwych słów
        """
        Generate all strings from the given words and letters from the given alphabet within the given lev_dist from 'word'.
        We assume that distance(word1, word2) = 0 only if word1 == word2.
        Various distance generation functions can be applied - eg. Levenshtein, Damerau–Levenshtein, Hamming etc.
        :param word: word: seed for the generation of strings
        :param max_dist: maximum distance between generated string and given word (inclusive)
        :return: set of edits that are one edit away from `word`
        """
        if max_dist < 0:
            raise ValueError("max_dist cannot be negative")

        # distance(word1, word2) = 0 only if word1 == word2
        if max_dist == 0:
            return {word}

        # set of strings s_i meeting condition: distance(s_i, word) = 1 with the given dist_1_generation_fun
        output_set = self._damerau_levenshtein_edits1(word)
        # candidates to lowercase
        output_set = set(map(lambda elem: elem.lower(), output_set))
        # if there is a filter function then filter the results
        if self.correct_word_predicate:
            output_set = set(filter(self.correct_word_predicate, output_set))

        # if the max_dist > 1 iteratively generate next sets (with growing distance)
        for _ in range(max_dist - 1):
            output_set = set(e2 for e1 in output_set for e2 in self._damerau_levenshtein_edits1(e1))
            # if fun_is_word_correct is not None then filter the results
            if self.correct_word_predicate:
                output_set = set(filter(self.correct_word_predicate, output_set))
            # candidates to lowercase
            output_set = set(map(lambda elem: elem.lower(), output_set))

        return output_set

    def _damerau_levenshtein_edits1(self, word):
        # generowanie ciągów znaków odległych o 1 od zadanego słowa
        """
        SOURCE: Norvig's article: How to Write a Spelling Corrector.
        LINK: http://norvig.com/spell-correct.html
        METRICS: Damerau–Levenshtein distance
        :param word: seed for the generation of strings
        :return: set of edits that are one edit away from `word`
        """
        # generate all possible splits of a word
        # eg. "kot" -> [('', 'kot'), ('k', 'ot'), ('ko', 't'), ('kot', '')]
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        # generate all possible deletions - removing first letter of each right split of the word and adding to left
        # eg. "kot" -> ['ot', 'kt', 'ko']
        if self.is_deleting:
            deletes = [L + R[1:] for L, R in splits if R]
        else:
            deletes = []

        # generate all possible transposes (transpose = switching 2 adjoin letters in a word)
        # eg. "kot" -> ['okt', 'kto']
        if self.is_transposing:
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        else:
            transposes = []

        # generate all possible replaces of first character of the right slice with letters from the given alphabet
        # eg. "kot" -> ['aot', 'ąot', 'bot', 'cot', ... ]
        if self.is_replacing:
            replaces = [L + c + R[1:] for L, R in splits if R for c in self.alphabet]
        else:
            replaces = []

        # generate all possible insertions of with letters from the given alphabet
        # eg. "kot" -> ['akot', 'ąkot', 'bkot', 'ckot', ... ]
        if self.is_inserting:
            inserts = [L + c + R for L, R in splits for c in self.alphabet]
        else:
            inserts = []

        return set(deletes + transposes + replaces + inserts)