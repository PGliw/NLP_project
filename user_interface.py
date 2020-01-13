from spell_correction import SpellingCorrector


if __name__ == '__main__':

    sc = SpellingCorrector()

    # POBIERANIE Z KLAWIATURY:
    print()
    print("*********************************************")
    print("*******      Witaj w programie         ******")
    print("*********************************************")

    word = input('Wprowadź słowo: ')
    edit_distance = int(input('Podaj odległość Levensteina (0-4): '))
    enter_error_type = input('Czy chcesz wybrać typ błędu? [Y/N] ')
    if enter_error_type.lower() == 'y':
        print('Wprowadź które z typów będów chcesz poprawić')
        print('[1] Wstawiono przypadkowo dodatkową literkę')
        print('[2] Zamieniono 2 sąsiadujące litery')
        print('[3] Popełniono literówkę (użyto innej litery niż trzeba)')
        print('[4] "Zjedzono" literę')
        print('Np. 124 - oznacza opcje 1, 2 i 4 (bez 3)')
        options = input('Wprowadź numery opcji: ')
        if '1' in options:
            sc.word_generator.is_deleting = True
        else:
            sc.word_generator.is_deleting = False
        if '2' in options:
            sc.word_generator.is_transposing = True
        else:
            sc.word_generator.is_transposing = False
        if '3' in options:
            sc.word_generator.is_replacing = True
        else:
            sc.word_generator.is_replacing = False
        if '4' in options:
            sc.word_generator.is_inserting = True
        else:
            sc.word_generator.is_inserting = False

    result = sc.correct_phrase(word, edit_distance, True)
    for i, el in enumerate(result[1]):
        print(i, el)
