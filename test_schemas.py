import unittest

from schemas import (
    AnalogySchema,
    EmbeddingSchema,
    NeighboursSchema,
    VectorSchema
)


class SchemasTest(unittest.TestCase):
    def test_vector_schema(self):
        word = "bad"
        vector = [1., 2., 3.]
        VectorSchema().load({
            'word': word,
            'vector': vector,
        })

    def test_neighbours_schema(self):
        words = ["bad", "sad", "glad"]
        n = 2
        neighbours = [[("horrible", 0.8), ("horrific", 0.75)],
                      [("melancholy", 0.9), ("disappointed", 0.85)],
                      [("happy", 0.81), ("joyful", 0.74)]]
        NeighboursSchema().load({
            'words': words,
            'n': n,
            'neighbours': neighbours,
        })

    def test_analogy_schema(self):
        a = "man"
        b = "waiter"
        c = "woman"
        n = 2
        completions = [("waiter", 0.8),
                       ("actress", 0.5)]
        AnalogySchema().load({
            'a': a,
            'b': b,
            'c': c,
            'n': n,
            'completions': completions,
        })

    def test_embeddings_schema(self):
        words = ["bad", "sad", "glad"]
        n = 2
        words_list = ["bad", "horrible", "horrific",
                      "sad", "melancholy", "disappointed",
                      "glad", "happy", "joyful"]
        embeddings_list = [[0.1, 0.1], [0.11, 0.11], [0.111, 0.111],
                           [0.2, 0.2], [0.22, 0.22], [0.222, 0.222],
                           [0.3, 0.3], [0.33, 0.33], [0.333, 0.333]]
        EmbeddingSchema().load({
            'words': words,
            'n': n,
            'words_list': words_list,
            'embeddings_list': embeddings_list,
        })


if __name__ == "__main__":
    unittest.main()
