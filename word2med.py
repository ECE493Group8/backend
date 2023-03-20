from typing import List, Tuple

import numpy as np
from sklearn.manifold import TSNE

from models.word2vec import MalamudWord2Vec


class Word2Med:
    """The Word2Med model from a saved Word2Vec Gensim model"""

    EMBEDDING_DIMENSION = 2
    TSNE_PERPLEXITY = 30.0

    def __init__(self, model_path: str):
        self.model = MalamudWord2Vec.load(model_path)

    def get_vector(self, word: str) -> List[float]:
        """Get the closest n words to the given word.

        Args:
            word (str): The word to retrieve the vector for.

        Returns:
            List[float]: A list of floats representing the vector of the given
                word.

        Raises:
            KeyError if the word is not in the model's vocabulary.
        """
        return self.model.wv[word].tolist()

    def get_n_closest(self,
                      words: List[str],
                      n: int) -> List[List[Tuple[str, float]]]:
        """Get the closest n words to each word in the given list of words.

        Args:
            words (List[str]): The words to retrieve the closest words to.

        Returns:
            List[List[Tuple[str, float]]]: A list of the same size as the number
                of given words. The list contains lists of size n for each given
                word. The lists of size n contain 2-tuples with the first
                element in the tuple being the neighbour word and the second
                element being the cosine similarity. The list of size n is
                sorted in descending order of cosine similarity.

        Raises:
            KeyError if the word is not in the model's vocabulary.
        """
        return [self.model.wv.most_similar(word, topn=n) for word in words]

    def complete_analogy(self, a: str, b: str, c: str, n: int) -> List[Tuple[str, float]]:
        """Completes the analogy "a is to b as c is to ...".

        Args:
            a (str): The first word in the analogy.
            b (str): The second word in the analogy.
            c (str): The third word in the analogy.
            n (int): The number of words to return.

        Returns:
            List[Tuple[str, float]]: A list of size n containing 2-tuples with
                the first element in the tuple being the word that completes the
                analogy and the second element being the cosine similarity. The
                list is sorted in descending order of cosine similarity.

        Raises:
            KeyError if the word is not in the model's vocabulary.
        """
        return self.model.wv.most_similar(positive=[a, c], negative=[b], topn=n)

    def get_embeddings(self,
                       words: List[str],
                       n: int) -> List[List[Tuple[str, List[float]]]]:
        """Returns 2-dimensional vectors of ***

        Raises:
            KeyError if the word is not in the model's vocabulary.
            ValueError if the number of words to embed is less than
                TSNE_PERPLEXITY.
        """
        words_list = []
        vectors_list = []
        for word in words:
            # Append the current word and its vector to the word list and vector
            # list.
            words_list.append(word)
            vectors_list.append(self.model.wv[word])
            # For each similar word to the current word, append the similar word
            # and its vector to the word list and vector list.
            for similar_word, _ in self.model.wv.most_similar(word, topn=n):
                words_list.append(similar_word)
                vectors_list.append(self.model.wv[similar_word])

        # We have to have at least TSNE_PERPLEXITY vectors to embed in order for
        # TSNE to work. Ensure that this requirement is met.
        if len(vectors_list) < int(Word2Med.TSNE_PERPLEXITY):
            raise ValueError("Not enough samples provided")

        vectors = np.array(vectors_list)

        # Embed the vectors.
        tsne = TSNE(n_components=Word2Med.EMBEDDING_DIMENSION,
                    perplexity=Word2Med.TSNE_PERPLEXITY,
                    random_state=0)
        embedded_vectors = tsne.fit_transform(vectors)
        embedded_vectors_list = embedded_vectors.tolist()

        return words_list, embedded_vectors_list


if __name__ == "__main__":
    # TODO: Design proper tests for this eventually.

    m = Word2Med("./trained_models/test/test.model")

    from pprint import pprint

    pprint(m.get_vector("bad"))
    pprint(m.get_n_closest(["bad", "sucky", "good", "great"], 2))
    print(m.complete_analogy("man", "waiter", "woman", 2))
    pprint(m.get_embeddings(["bad", "sucky", "good", "great"], 10))
