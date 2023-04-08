import pytest

from backend import app

# TODO: May have to add content-type: json header to responses for response.json to work

def test_vector():
    response = app.test_client().get('/vector?word=pain')
    print(response)
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['word', 'vector'])

def test_vector_err_no_words():
    response = app.test_client().get('/vector?word=')
    print(response)
    assert response.status_code == 500

def test_neighbours_single_word():
    response = app.test_client().get('/neighbours?words=pain&n=5')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'neighbours'])

def test_neighbours_multiple_words():
    response = app.test_client().get('/neighbours?words=pain&words=cancer&n=5')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'neighbours'])

def test_neighbours_err_no_words():
    response = app.test_client().get('/neighbours?&n=5')
    assert response.status_code == 500

def test_neighbours_err_no_num():
    response = app.test_client().get('/neighbours?words=pain&')
    assert response.status_code == 500

def test_neighbours_err_invalid_num():
    response = app.test_client().get('/neighbours?words=pain&n=0')
    assert response.status_code == 500

def test_analogy():
    response = app.test_client().get('/analogy?a=chemotherapy&b=cancer&c=alzheimer&n=10')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['a', 'b', 'c', 'n', 'completions'])

def test_analogy_err_not_enough_words():
    response = app.test_client().get('/analogy?a=chemotherapy&b=cancer&n=10')
    assert response.status_code == 500

def test_analogy_err_blank_word():
    response = app.test_client().get('/analogy?a=chemotherapy&b=cancer&c=&n=10')
    assert response.status_code == 500

def test_analogy_no_num():
    response = app.test_client().get('/analogy?a=chemotherapy&b=cancer&c=alzheimer')
    assert response.status_code == 500

def test_analogy_err_invalid_num():
    response = app.test_client().get('/analogy?a=chemotherapy&b=cancer&c=alzheimer&n=0')
    assert response.status_code == 500

def test_embeddings_multiple_words():
    response = app.test_client().get('/embeddings?words=pain&words=back&words=boy&n=10')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'words_list', 'embeddings_list'])

def test_embeddings_err_not_enough_words():
    response = app.test_client().get('/embeddings?words=pain&words=back&n=10')
    assert response.status_code == 500

def test_embeddings_err_no_num():
    response = app.test_client().get('/embeddings?words=pain&words=back&words=boy')
    assert response.status_code == 500

def test_embeddings_err_invalid_num():
    response = app.test_client().get('/embeddings?words=pain&words=back&words=boy&n=3')
    assert response.status_code == 500
