import pytest

from backend import app

# TODO: May have to add content-type: json header to responses for response.json to work

def test_vector():
    response = app.test_client().get('/vector?word=word1')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['word', 'vector'])

def test_neighbours_single_word():
    response = app.test_client().get('/neighbours?words=word1&n=5')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'neighbours'])

def test_neighbours_multiple_words():
    response = app.test_client().get('/neighbours?words=word1&words=word2&n=5')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['a', 'b', 'c', 'n', 'completions'])

def test_analogy():
    response = app.test_client().get('/analogy?a=worda&b=wordb&c=wordc&n=10')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['a', 'b', 'c', 'n', 'completions'])

def test_embeddings_single_word():
    response = app.test_client().get('/embeddings?words=word1&n=5')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'words_list', 'embeddings_list'])

def test_embeddings_multiple_words():
    response = app.test_client().get('/embeddings?words=word1&words=word2&n=5')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'words_list', 'embeddings_list'])

