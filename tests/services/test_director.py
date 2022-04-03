from unittest import mock

import pytest

from service.director import DirectorNotFound
from pytest_lazyfixture import lazy_fixture


@pytest.fixture
def directors_list():
    return [
        {
            'id': 1,
            'name': mock.ANY,
        },
        {
            'id': 2,
            'name': mock.ANY,
        },
    ]


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
def test_get_one(director_service, data):
    director_service.dao.get_one.return_value = data

    assert director_service.get_one(data['id']) == data

# тестируем ошибку в сервисе
def test_get_one_with_error(director_service):
    with pytest.raises(DirectorNotFound): # .side_effect
        director_service.get_one(0)


@pytest.mark.parametrize(
    'length, data',
    (
        (
            2,
            lazy_fixture('directors_list'),
        ),
        (
            0,
            [],
        ),
    ),
)
def test_get_all(director_service, length, data):
    director_service.dao.get_all.return_value = data

    test_result = director_service.get_all()
    assert isinstance(test_result, list)
    assert len(test_result) == length
    assert test_result == data


@pytest.mark.parametrize(
    'original_data, modified_data',
    (
        (
            {
                'id': 1,
                'name': 'test',
            },
            {
                'id': 1,
                'name': 'changed_name',
            },
        ),
    )
)
def test_partially_update(director_service, original_data, modified_data):
    director_service.dao.get_one.return_value = original_data
    director_service.partially_update(modified_data)
    # тест вызова ГЕТ_1 с НЕмодиф.ДАННЫМИ
    director_service.dao.get_one.assert_called_once_with(original_data['id'])
    # тест вызова АПДЕЙТ с модиф.ДАННЫМИ
    director_service.dao.update.assert_called_once_with(modified_data)


@pytest.mark.parametrize(
    'original_data, modified_data',
    (
        (
            {
                'id': 1,
                'name': mock.ANY,
            },
            {
                'id': 1,
                'wrong_field': mock.ANY,
            },
        ),
    )
)
# частичное обновление с ошибочными полями
def test_partially_update_with_wrong_fields(director_service, original_data, modified_data):
    director_service.dao.get_one.return_value = original_data

    director_service.partially_update(modified_data)
    # тест вызова АПДЕЙТ с НЕмодиф.ДАННЫМИ
    director_service.dao.update.assert_called_once_with(original_data)


@pytest.mark.parametrize(
    'director_id',
    (
        1,
    )
)
def test_delete(director_service, director_id):
    director_service.delete(director_id)
    # проверим, что ДАО был вызван 1 раз с тем-же ИД
    director_service.dao.delete.assert_called_once_with(director_id)


@pytest.mark.parametrize(
    'director_data',
    (
        (
            {
                'id': mock.ANY,
                'name': mock.ANY,
            },
        )
    )
)
def test_update(director_service, director_data):
    director_service.update(director_data)
    # проверим, что ДАО был вызван 1 раз с тем-же ИД
    director_service.dao.update.assert_called_once_with(director_data)
