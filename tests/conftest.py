from unittest import mock
from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from service.director import DirectorService
# 1 - импортируем сервис, кот. будем тестировать
from dao.genre import GenreDAO
from service.genre import GenreService
# 1 - импортируем сервис, кот. будем тестировать
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture
def director_dao():
    dao = DirectorDAO(None)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    return dao


@pytest.fixture
def director_service(director_dao):
    return DirectorService(dao=director_dao)


# 2 - создаем фикстуру
@pytest.fixture
def genre_dao():
    dao = GenreDAO(None)
    # 3 - подменяем методы DAO на MagicMock(ставим заглушку)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    return dao  # вернем заглушку


# 4 - инициализируем сервис на основе МОКов
@pytest.fixture
def genre_service(genre_dao):
    return GenreService(dao=genre_dao)


# 2 - создаем фикстуру
@pytest.fixture
def movie_dao():
    dao = MovieDAO(None)
    # 3 - подменяем методы DAO на MagicMock(ставим заглушку)
    dao.get_one = MagicMock()
    dao.get_all = MagicMock()
    dao.update = MagicMock()
    dao.delete = MagicMock()
    dao.create = MagicMock()
    return dao  # вернем заглушку


# 4 - инициализируем сервис на основе МОКов
@pytest.fixture
def movie_service(movie_dao):
    return MovieService(dao=movie_dao)
