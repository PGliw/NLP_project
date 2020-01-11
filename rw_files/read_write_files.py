import math
import pickle
import time

import dawg

frequency_words = r'C:\Users\Filip\Desktop\Projekty\NLP_project\frequency_list_base.txt'
pickle_file = 'polish_dictionary.dawg'

MAX_LINES = 20000


class CommaSeparatedFile:
    def __init__(self):
        self.filepath = r'C:\Users\Filip\Desktop\Projekty\NLP_project\slownik.txt'

    def split(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        number_of_files = math.floor(len(lines) / MAX_LINES)
        list_of_created_files = []
        for i in range(number_of_files):
            filename = f"slownik_czesc_{i+1}.txt"
            if i == number_of_files:
                self._file_action('w', filename, lines[i * MAX_LINES:])
            else:
                self._file_action('w', filename, lines[i * MAX_LINES:(i + 1) * MAX_LINES])
            list_of_created_files.append(filename)
        return list_of_created_files

    @staticmethod
    def get_words(filepath):
        all_words = []
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                all_words = [*all_words, *line.strip().lower().split(',')]
        all_words = list(map(lambda s: s.replace(" ", ""), all_words))
        return all_words

    def _file_action(self, action, filename, contents):
        with open(filename, action, encoding='utf-8') as f:
            f.writelines(contents)
        print(f"ACTION: '{action}' on file {filename}")


class FrequencyFile(CommaSeparatedFile):
    def __init__(self):
        super().__init__()
        self.filepath = r'C:\Users\Filip\Desktop\Projekty\NLP_project\frequency_list_base.txt'

    @staticmethod
    def get_words(filepath):
        all_words = []
        with open(frequency_words, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[1:MAX_LINES]:
                all_words.append(tuple(line.strip().split(";")))
        return all_words
