from spell_correction import SpellingCorrector
from canditates_generator import WordGenerator
import time

if __name__ == '__main__':
    wg = WordGenerator()
    sc = SpellingCorrector()
    words = ['Kot', 'aaa', 'Bóbr', 'wraf', 'wierza']

    # Word generation benchmark
    for word in words:
        for dist in range(4):
            start = time.time()
            wg.generate_candidates(word, dist)
            end = time.time()
            print("Fraza:", word, ", Odległość:", dist,  ", Czas:", end - start)

    # Correction benchmark
    for word in words:
        for dist in range(5):
            start = time.time()
            sc.correct_phrase(word, dist, True)
            end = time.time()
            print("Fraza:", word, ", Odległość:", dist, ", Czas:", end - start)
