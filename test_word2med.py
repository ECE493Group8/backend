import unittest

from word2med import Word2Med


class Word2MedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = Word2Med("./trained_models/test/test.model")

    def test_get_vector(self):
        word = "bad"
        vector = self.model.get_vector(word)
        self.assertIsInstance(vector, list)
        self.assertIsInstance(vector[0], float)

    def test_get_n_closest(self):
        words = ["bad", "sad", "glad"]
        n = 2
        result = self.model.get_n_closest(words, n)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(words))
        for neighbours in result:
            self.assertIsInstance(neighbours, list)
            self.assertEqual(len(neighbours), n)
            self.assertIsInstance(neighbours[0], tuple)
            self.assertEqual(len(result[0]), 2)
            self.assertIsInstance(neighbours[0][0], str)
            self.assertIsInstance(neighbours[0][1], float)

    def test_complete_analogy(self):
        a = "man"
        b = "waiter"
        c = "woman"
        n = 2
        result = self.model.complete_analogy(a, b, c, n)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), n)
        self.assertIsInstance(result[0], tuple)
        self.assertEqual(len(result[0]), 2)
        self.assertIsInstance(result[0][0], str)
        self.assertIsInstance(result[0][1], float)

    def test_get_embeddings(self):
        words = ["bad", "sad", "glad"]
        n = 12
        words_list, embedded_vectors_list = self.model.get_embeddings(words, n)

        self.assertIsInstance(words_list, list)
        self.assertIsInstance(words_list[0], str)
        self.assertEqual(len(words_list), (n + 1) * len(words))

        self.assertIsInstance(embedded_vectors_list, list)
        self.assertIsInstance(embedded_vectors_list[0], list)
        self.assertIsInstance(embedded_vectors_list[0][0], float)
        self.assertEqual(len(embedded_vectors_list), (n + 1) * len(words))
        self.assertEqual(len(embedded_vectors_list[0]), 2)  # 2-dimensional embedding
