import pickle
import time

import dawg

from rw_files.read_write_files import CommaSeparatedDictionary


class MyDawg:
    def __init__(self, file_handler=CommaSeparatedDictionary()):
        self.file_handler = file_handler

    def create_dawgs(self, list_of_filepaths, force_pickle=True):
        all_dawgs = []
        for file in list_of_filepaths:
            s_time = time.time()
            words = self.file_handler.get_words(file)
            base_dawg = dawg.DAWG(words)
            completion_dawg = dawg.CompletionDAWG(words)
            all_dawgs.append((base_dawg, completion_dawg))

            print(
                f"Created DAWGs {list_of_filepaths.index(file) + 1}/{len(list_of_filepaths)} "
                f"| TIME: {time.time() - s_time}")
            
            if force_pickle:
                self.pickle_dawg(f"base_dawg_{list_of_filepaths.index(file) + 1}.pkl", base_dawg)
                self.pickle_dawg(f"completion_dawg_{list_of_filepaths.index(file) + 1}.pkl", completion_dawg)
        return all_dawgs

    @staticmethod
    def pickle_dawg(filename, contents):
        s_time = time.time()
        with open(filename, 'wb') as f:
            pickle.dump(contents, f)
        print(f"Pickled to {filename} | TIME: {time.time() - s_time}")

    @staticmethod
    def unpickle_dawg(filename):
        s_time = time.time()
        with open(filename, 'rb') as f:
            loaded_obj = pickle.load(f)
        print(f"Unpickled from {filename} | TIME: {time.time() - s_time}")
        return loaded_obj

    @staticmethod
    def is_word(b_dawg, word):
        return word.lower() in b_dawg

    @staticmethod
    def get_prefixes(b_dawg, word):
        for prefix in b_dawg.iterprefixes(word.lower()):
            print(prefix)
        return b_dawg.prefixes(word.lower())

    @staticmethod
    def is_word_with_prefix(c_dawg, prefix):
        return c_dawg.has_keys_with_prefix(prefix.lower())
