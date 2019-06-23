from recipes import RecipeDAO
from unittest.mock import patch, mock_open


class TestRecipeDAO(object):

    def test_import_loads_recipes(self):
        # Arrange
        DAO = RecipeDAO()
        data = 'id,fieldA,fieldB,fieldC\n1,data1A,"data 1B",123\n2,data2A,"data 2B",456\n'
        # mock_open only supports __iter__ from python 3.7.1, so patching here
        m_open = mock_open(read_data=data)
        m_open.return_value.__iter__ = lambda self: self
        m_open.return_value.__next__ = lambda self: next(iter(self.readline, ''))

        # Act
        with patch('recipes.open', m_open):
            DAO.import_file('test_file')

        # Assert
        assert DAO.recipes == {
            1: {'id': 1, 'fieldA': 'data1A', 'fieldB': 'data 1B', 'fieldC': 123},
            2: {'id': 2, 'fieldA': 'data2A', 'fieldB': 'data 2B', 'fieldC': 456},
        }

    def test_import_loads_cuisines(self):
        # Arrange
        DAO = RecipeDAO()
        data = 'id,fieldA,recipe_cuisine\n1,data1,typeA\n2,data2,typeB\n3,data3,typeA\n'
        # mock_open only supports __iter__ from python 3.7.1, so patching here
        m_open = mock_open(read_data=data)
        m_open.return_value.__iter__ = lambda self: self
        m_open.return_value.__next__ = lambda self: next(iter(self.readline, ''))

        # Act
        with patch('recipes.open', m_open):
            DAO.import_file('test_file')

        # Assert
        assert DAO.cuisines == {
            'typeA': [
                {'id': 1, 'fieldA': 'data1', 'recipe_cuisine': 'typeA'},
                {'id': 3, 'fieldA': 'data3', 'recipe_cuisine': 'typeA'},
            ],
            'typeB': [
                {'id': 2, 'fieldA': 'data2', 'recipe_cuisine': 'typeB'},
            ]
        }
