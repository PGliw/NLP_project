import unittest
from canditates_generator import damerau_levenshtein_edits1, edits_n


class TestCandidatesGenerator(unittest.TestCase):
    polish_alphabet = 'aąbcćdeęfghijklmnoópqrsśtuvwxyzźż'

    def test_edits_n_0_equals(self):
        given = edits_n("kot", self.polish_alphabet, 0, damerau_levenshtein_edits1)
        expected = {"kot"}
        self.assertEqual(given, expected)

    def test_edits_n_1_equals(self):
        given = edits_n("kot", self.polish_alphabet, 1, damerau_levenshtein_edits1)
        expected = damerau_levenshtein_edits1("kot", self.polish_alphabet)
        self.assertEqual(given, expected)

    def test_edits_n_1_containing(self):
        given = edits_n("kot", self.polish_alphabet, 1, damerau_levenshtein_edits1)
        expected_values = {"zot", "okt", "kott", "ot"}
        for expected_value in expected_values:
            self.assertIn(expected_value, given)

    def test_edits_n_1_not_containing(self):
        given = edits_n("kot", self.polish_alphabet, 1, damerau_levenshtein_edits1)
        expected_values = {"zott", "otk", "kottt", "o"}
        for expected_value in expected_values:
            self.assertNotIn(expected_value, given)

    def test_edits_n_2_equals(self):
        given = edits_n("kot", self.polish_alphabet, 2, damerau_levenshtein_edits1)
        expected = set(e2 for e1 in damerau_levenshtein_edits1("kot", self.polish_alphabet) for e2 in
                       damerau_levenshtein_edits1(e1, self.polish_alphabet))
        self.assertEqual(given, expected)

    def test_edits_n_2_containing(self):
        given = edits_n("kot", self.polish_alphabet, 2, damerau_levenshtein_edits1)
        expected_values = {"ktoo", "k"}
        for expected_value in expected_values:
            self.assertIn(expected_value, given)

    def test_edits_n_2_not_containing(self):
        given = edits_n("kot", self.polish_alphabet, 2, damerau_levenshtein_edits1)
        expected_values = {"toko", "kotttt", ""}
        for expected_value in expected_values:
            self.assertNotIn(expected_value, given)


