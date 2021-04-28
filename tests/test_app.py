import os
import pytest

from app import create_app, db, models


@pytest.fixture
def client():
    os.environ['APP_CONFIG'] = 'testing.cfg'
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            db.session.add(models.Book(title='1984', author='George Orwell'))
            db.session.add(models.Book(title='Война и мир', author='Лев Толстой'))
            db.session.commit()

        yield client

        with app.app_context():
            db.drop_all()


def test_book_get_all(client):
    response = client.get('/book/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    authors = [book['author'] for book in data]
    assert 'George Orwell' in authors
    assert 'Лев Толстой' in authors
    titles = [book['title'] for book in data]
    assert '1984' in titles
    assert 'Война и мир' in titles


def test_post_new_book(client):
    response = client.post('/book/', json={
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
    })
    assert response.status_code == 200


def test_book_get_single(client):
    response = client.get('/book/1/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['author'] == 'George Orwell'
    assert data['title'] == '1984'


def test_update_book(client):
    response = client.put('/book/1/', json={
        'title': 'Мастер и Маргарита',
        'author': 'Михаил Булгаков',
    })
    assert response.status_code == 200

    response = client.get('/book/1/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)
    assert data['author'] == 'Михаил Булгаков'
    assert data['title'] == 'Мастер и Маргарита'


def test_delete_book(client):
    response = client.delete('/book/1/')
    assert response.status_code == 200

    response = client.get('/book/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    book = data[0]
    assert book['author'] == 'Лев Толстой'
    assert book['title'] == 'Война и мир'
