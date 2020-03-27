import unittest
from linguistic_processing import Preprocessor


class TestPreprocessingEnglish(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor("english")
        self.text = "Friends, Romans, Countrymen, lend me your ears;"

    def test_stopwords(self):
        actual = self.preprocessor.stopwords
        expected = ["and", "in", "he", "she"]
        self.assertTrue(len(set(expected) - set(actual)) == 0)

    def test_deaccenting(self):
        actual = self.preprocessor.strip_accents("touché")
        expected = "touche"
        self.assertEqual(expected, actual)

    def test_preprocessor(self):
        actual = self.preprocessor.preprocess(self.text)
        expected = ['friends', 'romans', 'countrymen', 'lend', 'ears']
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    test_classes_to_run = [TestPreprocessingEnglish]

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
