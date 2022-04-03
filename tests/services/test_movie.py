from unittest import mock

import pytest
from pytest_lazyfixture import lazy_fixture

@pytest.fixture
def movies_list():
    return [
        {
            'id': 111,
            'name': mock.ANY,
        },
        {
            'id': 222,
            'name': mock.ANY,
        },
    ]
# 7 - подключим фикстуры к тестированию
@pytest.mark.parametrize(
    'data',
    (
        {
            'id': 1,
            'name': mock.ANY,
        },
        {
            'id': 2,
            'name': mock.ANY,
        },
    )
)
# 5.2 - пишем тест с фикстурой parametrize на Сервис
def test_get_one2(movie_service, data):
    movie_service.dao.get_one.return_value = data
    #и организуем тестирование такой выдачи
    assert movie_service.get_one(data['id']) == data

@pytest.mark.parametrize(
    'length, data',
    (
        (
            2,
            lazy_fixture('movies_list')
        ),
        (
            0,
            [],
        ),
    ),
)
def test_get_all(movie_service, length, data):
    movie_service.dao.get_all.return_value = data

    test_result = movie_service.get_all()
    assert isinstance(test_result, list) # проверяем, что вернулся список
    assert len(test_result) == length # проверяем его длину
    assert test_result == data # проверяем сами данные на правильность

@pytest.mark.parametrize(
    'original_data, modified_data',
    (
        (
            {
                'id': 1,
                'title': 'movie_1',
                'description': mock.ANY,
                'trailer': mock.ANY,
            },
            {
                'id': 1,
                'title': 'changed_movie',
                'description': mock.ANY,
                'trailer': mock.ANY,
            },
        ),
    )
)
def test_partially_update(movie_service, original_data, modified_data):
    movie_service.dao.get_one.return_value = original_data
    movie_service.partially_update(modified_data)
    # тест вызова ГЕТ_1 с НЕмодиф.ДАННЫМИ
    movie_service.dao.get_one.assert_called_once_with(original_data['id'])
    # тест вызова АПДЕЙТ с модиф.ДАННЫМИ
    movie_service.dao.update.assert_called_once_with(modified_data)

@pytest.mark.parametrize(
    'movie_id',
    (
        1,
    )
)
def test_delete(movie_service, movie_id):
    movie_service.delete(movie_id)
    # проверим, что ДАО был вызван 1 раз с тем-же ИД
    movie_service.dao.delete.assert_called_once_with(movie_id)

@pytest.mark.parametrize(
    'movie_data',
    (
        (
            {
                'id': mock.ANY,
                'title': mock.ANY,
                'description': mock.ANY,
                'trailer': mock.ANY,
                'year': mock.ANY,
                'rating': mock.ANY,
                'genre_id': mock.ANY,
                'director_id': mock.ANY,
            },
        )
    )
)
def test_update(movie_service, movie_data):
    movie_service.update(movie_data)
    # проверим, что ДАО был вызван 1 раз с тем-же ИД
    movie_service.dao.update.assert_called_once_with(movie_data)