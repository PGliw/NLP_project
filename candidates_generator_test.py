import unittest
from canditates_generator import WordGenerator


class TestCandidatesGenerator(unittest.TestCase):
    word_generator = WordGenerator()

    def test_edits_n_0_equals(self):
        given = self.word_generator.generate_candidates("kot", 0)
        expected = {"kot"}
        self.assertEqual(given, expected)

    def test_edits_n_1_equals(self):
        given = self.word_generator.generate_candidates("kot", 1)
        expected = self.word_generator._damerau_levenshtein_edits1("kot")
        self.assertEqual(given, expected)

    def test_edits_n_1_containing(self):
        given = self.word_generator.generate_candidates("kot", 1)
        expected_values = {"zot", "okt", "kott", "ot"}
        for expected_value in expected_values:
            self.assertIn(expected_value, given)

    def test_edits_n_1_not_containing(self):
        given = self.word_generator.generate_candidates("kot", 1)
        expected_values = {"zott", "otk", "kottt", "o"}
        for expected_value in expected_values:
            self.assertNotIn(expected_value, given)

    def test_edits_n_2_equals(self):
        given = self.word_generator.generate_candidates("kot", 2)
        expected = set(e2 for e1 in self.word_generator._damerau_levenshtein_edits1("kot") for e2 in
                       self.word_generator._damerau_levenshtein_edits1(e1))
        self.assertEqual(given, expected)

    def test_edits_n_2_containing(self):
        given = self.word_generator.generate_candidates("kot", 2)
        expected_values = {"ktoo", "k"}
        for expected_value in expected_values:
            self.assertIn(expected_value, given)

    def test_edits_n_2_not_containing(self):
        given = self.word_generator.generate_candidates("kot", 2)
        expected_values = {"toko", "kotttt", ""}
        for expected_value in expected_values:
            self.assertNotIn(expected_value, given)
