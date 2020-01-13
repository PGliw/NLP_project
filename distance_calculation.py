import numpy as np


def damerau_levenshtein_distance(seq1, seq2):
    """
    SOURCE: https://gist.github.com/pombredanne/0d83ad58f45986ddeb0917266e106be0
    :param seq1 string
    :param seq2 string
    :return: Damerau-Levenshtein distance between sequences seq1 and seq2
    """
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    INF = len(seq1) + len(seq2)

    # Matrix: (M + 2) x (N + 2)
    matrix = [[INF for n in range(len(seq2) + 2)]]
    matrix += [[INF] + list(range(len(seq2) + 1))]
    matrix += [[INF, m] + [0] * len(seq2) for m in range(1, len(seq1) + 1)]

    # Holds last row each element was encountered: DA in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for row in range(1, len(seq1) + 1):
        # Current character in a
        ch_a = seq1[row - 1]

        # Column of last match on this row: DB in pseudocode
        last_match_col = 0

        for col in range(1, len(seq2) + 1):
            # Current character in b
            ch_b = seq2[col - 1]

            # Last row with matching character
            last_matching_row = last_row.get(ch_b, 0)

            # Cost of substitution
            cost = 0 if ch_a == ch_b else 1

            # Compute substring distance
            matrix[row + 1][col + 1] = min(
                matrix[row][col] + cost,  # Substitution
                matrix[row + 1][col] + 1,  # Addition
                matrix[row][col + 1] + 1,  # Deletion

                # Transposition
                # Start by reverting to cost before transposition
                matrix[last_matching_row][last_match_col]
                # Cost of letters between transposed letters
                # 1 addition + 1 deletion = 1 substitution
                + max((row - last_matching_row - 1),
                      (col - last_match_col - 1))
                # Cost of the transposition itself
                + 1)

            # If there was a match, update last_match_col
            if cost == 0:
                last_match_col = col

        # Update last row for current character
        last_row[ch_a] = row

    # Return last element
    return matrix[-1][-1]


def levenshtein_distance(seq1, seq2):
    """
    Source: https://stackabuse.com/levenshtein-distance-and-text-similarity-in-python/
    :param seq1 string
    :param seq2 string
    :returns levenshtein distance between seq1 and seq2 (number)
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
