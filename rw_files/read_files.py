import pickle
import dawg

comma_separated_words = r'C:\Users\Filip\Desktop\Projekty\NLP_project\slownik.txt'
frequency_words = r'C:\Users\Filip\Desktop\Projekty\NLP_project\frequency_list_base.txt'
pickle_file = 'polish_dictionary.dawg'

MAX_LINES = 10000


def get_words_from_commaseparated_file():
    all_words = []
    with open(comma_separated_words, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[:MAX_LINES]:
            all_words = [*all_words, *line.strip().lower().split(',')]
    all_words = list(map(lambda s: s.replace(" ", ""), all_words))
    return all_words


def get_words_from_frequency_file():
    all_words = []
    with open(frequency_words, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:MAX_LINES]:
            all_words.append(tuple(line.strip().split(";")))
    return all_words


def is_word(b_dawg, word):
    return word.lower() in b_dawg


def get_prefixes(b_dawg, word):
    for prefix in b_dawg.iterprefixes(word.lower()):
        print(prefix)
    return b_dawg.prefixes(word.lower())


def is_word_with_prefix(c_dawg, prefix):
    return c_dawg.has_keys_with_prefix(prefix.lower())


def pickle_dawg(obj):
    with open(pickle_file, 'wb') as f:
        pickle.dump(obj, f)


def unpickle_dawg():
    with open(pickle_file, 'rb') as f:
        loaded_obj = pickle.load(f)
    return loaded_obj


array = get_words_from_commaseparated_file()
array_csv = get_words_from_frequency_file()

base_dawg = dawg.DAWG(array)
# completion_dawg = dawg.CompletionDAWG(array)

pickle_dawg(array)
unpickle_dawg()
