from unittest import mock

import pytest
from pytest_lazyfixture import lazy_fixture

@pytest.fixture
def genres_list():
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
            'name': "second name",#mock.ANY,
        },
    )
)

# 5.1 - пишем тест на Сервис (без parametrize)
# def test_get_one(genre_service):
#     # можем сразу настроить ДАО на выдачу определенных данных
#     genre_service.dao.get_one.return_value = {
#         'id': 1,
#         'name': 'test',
#     }
#     #и организуем тестирование такой выдачи
#     assert genre_service.get_one(1) == {
#         'id': 1,
#         'name': 'test',
#     }

# 5.2 - пишем тест с фикстурой parametrize на Сервис
def test_get_one2(genre_service, data):
    genre_service.dao.get_one.return_value = data
    #и организуем тестирование такой выдачи
    assert genre_service.get_one(data['id']) == data


@pytest.mark.parametrize(
    'length, data',
    (
        (
            2,
            lazy_fixture('genres_list')
        ),
        (
            0,
            [],
        ),
    ),
)
def test_get_all(genre_service, length, data):
    genre_service.dao.get_all.return_value = data

    test_result = genre_service.get_all()
    assert isinstance(test_result, list) # проверяем, что вернулся список
    assert len(test_result) == length # проверяем его длину
    assert test_result == data # проверяем сами данные на правильность

@pytest.mark.parametrize(
    'original_data, modified_data',
    (
        (
            {
                'id': 1,
                'name': 'genre_1',
            },
            {
                'id': 1,
                'name': 'changed_genre',
            },
        ),
    )
)
def test_partially_update(genre_service, original_data, modified_data):
    genre_service.dao.get_one.return_value = original_data
    genre_service.partially_update(modified_data)
    # тест вызова ГЕТ_1 с НЕмодиф.ДАННЫМИ
    genre_service.dao.get_one.assert_called_once_with(original_data['id'])
    # тест вызова АПДЕЙТ с модиф.ДАННЫМИ
    genre_service.dao.update.assert_called_once_with(modified_data)

@pytest.mark.parametrize(
    'genre_id',
    (
        1,
    )
)
def test_delete(genre_service, genre_id):
    genre_service.delete(genre_id)
    # проверим, что ДАО был вызван 1 раз с тем-же ИД
    genre_service.dao.delete.assert_called_once_with(genre_id)


@pytest.mark.parametrize(
    'genre_data',
    (
        (
            {
                'id': mock.ANY,
                'name': mock.ANY,
            },
        )
    )
)
def test_update(genre_service, genre_data):
    genre_service.update(genre_data)
    # проверим, что ДАО был вызван 1 раз с тем-же ИД
    genre_service.dao.update.assert_called_once_with(genre_data)