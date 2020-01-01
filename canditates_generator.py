def generate_candidates(word, l_dist):
    """"
    Generates candidates for correction for 'word' within l_dist distance
    using Polish alphabet and Damerau-Levenstein's distance
    @:param word - word to be corrected
    @:param l_dist - maximum Damerau-Levenstein's distance between generated correction c_i and given word w
    @:returns set of generated strings within the given levenstein distance from given word
    """
    return edits_n(word=word, alphabet='aąbcćdeęfghijklmnoópqrsśtuvwxyzźż', max_dist=l_dist,
                   dist_1_generation_fun=damerau_levenshtein_edits1)


def damerau_levenshtein_edits1(word, alphabet):
    """
    SOURCE: Norvig's article: How to Write a Spelling Corrector.
    LINK: http://norvig.com/spell-correct.html
    METRICS: Damerau–Levenshtein distance
    :param word: seed for the generation of strings
    :param alphabet: alphabet used to generate strings from given word
    :return: set of edits that are one edit away from `word`
    """
    # generate all possible splits of a word
    # eg. "kot" -> [('', 'kot'), ('k', 'ot'), ('ko', 't'), ('kot', '')]
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    # generate all possible deletions - removing first letter of each right split of the word and adding to left
    # eg. "kot" -> ['ot', 'kt', 'ko']
    deletes = [L + R[1:] for L, R in splits if R]

    # generate all possible transposes (transpose = switching 2 adjoin letters in a word)
    # eg. "kot" -> ['okt', 'kto']
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]

    # generate all possible replaces of first character of the right slice with letters from the given alphabet
    # eg. "kot" -> ['aot', 'ąot', 'bot', 'cot', ... ]
    replaces = [L + c + R[1:] for L, R in splits if R for c in alphabet]

    # generate all possible insertions of with letters from the given alphabet
    # eg. "kot" -> ['akot', 'ąkot', 'bkot', 'ckot', ... ]
    inserts = [L + c + R for L, R in splits for c in alphabet]

    return set(deletes + transposes + replaces + inserts)


def edits_n(word, alphabet, max_dist, dist_1_generation_fun):
    """
    Generate all strings from the given words and letters from the given alphabet within the given lev_dist from 'word'.
    We assume that distance(word1, word2) = 0 only if word1 == word2.
    Various distance generation functions can be applied - eg. Levenshtein, Damerau–Levenshtein, Hamming etc.
    :param word: word: seed for the generation of strings
    :param alphabet: alphabet used for word generation
    :param max_dist: maximum distance between generated string and given word (inclusive)
    :param dist_1_generation_fun: function (word, alphabet) -> {strings} for generation set of strings within dist=1
    :return: set of edits that are one edit away from `word`
    """
    if max_dist < 0:
        raise ValueError("max_dist cannot be negative")

    # distance(word1, word2) = 0 only if word1 == word2
    if max_dist == 0:
        return {word}

    # set of strings s_i meeting condition: distance(s_i, word) = 1 with the given dist_1_generation_fun
    output_set = dist_1_generation_fun(word, alphabet)

    # if the max_dist > 1 iteratively generate next sets (with growing distance)
    for _ in range(max_dist - 1):
        output_set = set(e2 for e1 in output_set for e2 in dist_1_generation_fun(e1, alphabet))

    return output_set
