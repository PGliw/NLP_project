import math
import os
MAX_LINES = 20000


class CommaSeparatedDictionary:
    def __init__(self):
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.filepath = os.path.join(self.abs_path, 'slownik.txt')

    def split(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        number_of_files = math.floor(len(lines) / MAX_LINES)
        list_of_created_files = []
        for i in range(number_of_files):
            filepath = os.path.join(self.filepath, "split_dictionaries", f"slownik_czesc_{i+1}.txt")
            if i == number_of_files:
                self._file_action('w', filepath, lines[i * MAX_LINES:])
            else:
                self._file_action('w', filepath, lines[i * MAX_LINES:(i + 1) * MAX_LINES])
            list_of_created_files.append(filepath)
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
        print(f"ACTION: '{action}' | FILE: {filename}")


class FrequencyDictionary(CommaSeparatedDictionary):
    def __init__(self):
        super().__init__()
        self.filepath = os.path.join(self.abs_path, 'frequency_list_base.txt')

    def get_words(self):
        all_words = []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                all_words.append(tuple(line.strip().split(";")))
        return all_words
