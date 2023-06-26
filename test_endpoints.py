import pytest

from backend import app

TEST_MODEL_ID = "model_test"

# TODO: May have to add content-type: json header to responses for response.json to work

def test_vector():
    response = app.test_client().get(f'/vector?word=pain&model={TEST_MODEL_ID}')
    print(response)
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['word', 'model', 'vector'])

def test_vector_err_no_words():
    response = app.test_client().get(f'/vector?word=&model={TEST_MODEL_ID}')
    print(response)
    assert response.status_code == 500

def test_neighbours_single_word():
    response = app.test_client().get(f'/neighbours?words=pain&n=5&model={TEST_MODEL_ID}')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'model', 'neighbours'])

def test_neighbours_multiple_words():
    response = app.test_client().get(f'/neighbours?words=pain&words=cancer&n=5&model={TEST_MODEL_ID}')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'model', 'neighbours'])

def test_neighbours_err_no_words():
    response = app.test_client().get(f'/neighbours?&n=5&model={TEST_MODEL_ID}')
    assert response.status_code == 500

def test_neighbours_err_no_num():
    response = app.test_client().get(f'/neighbours?words=pain&model={TEST_MODEL_ID}&')
    assert response.status_code == 500

def test_analogy():
    response = app.test_client().get(f'{TEST_MODEL_ID}')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['a', 'b', 'c', 'n', 'model', 'completions'])

def test_analogy_err_not_enough_words():
    response = app.test_client().get(f'/analogy?a=chemotherapy&b=cancer&n=10&model={TEST_MODEL_ID}')
    assert response.status_code == 500

def test_analogy_err_blank_word():
    response = app.test_client().get(f'/analogy?a=chemotherapy&b=cancer&c=&n=10&model={TEST_MODEL_ID}')
    assert response.status_code == 500

def test_analogy_no_num():
    response = app.test_client().get(f'/analogy?a=chemotherapy&b=cancer&c=alzheimer&model={TEST_MODEL_ID}')
    assert response.status_code == 500

def test_embeddings_multiple_words():
    response = app.test_client().get(f'/embeddings?words=pain&words=back&words=boy&n=10&model={TEST_MODEL_ID}')
    assert response.status_code == 200
    assert all(key in dict(response.json) for key in ['words', 'n', 'words_list', 'model', 'embeddings_list'])

def test_embeddings_err_not_enough_words():
    response = app.test_client().get(f'/embeddings?words=pain&words=back&n=10&model={TEST_MODEL_ID}')
    assert response.status_code == 500

def test_embeddings_err_no_num():
    response = app.test_client().get(f'/embeddings?words=pain&words=back&words=boy&model={TEST_MODEL_ID}')
    assert response.status_code == 500
