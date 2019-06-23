from behave import given, when, then
from app import DAO
from datetime import datetime
from mock import patch, Mock
import json


@given('I am an API client')
def step_impl(context):
    pass


@when(u'I fetch a recipe by ID')
def step_impl(context):
    context.response = context.client.get('/recipes/1')


@then(u'I can see recipe fields')
def step_impl(context):
    data = context.response.get_json()
    recipe = DAO.get(1)
    assert data['id'] == 1
    for field, value in recipe.items():
        if field in ['created_at', 'updated_at']:
            value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').isoformat() + '+00:00'
        assert data[field] == value, f"{data[field]} == {value}"


@when(u'I fetch a recipe by cuisine')
def step_impl(context):
    mock_by_cuisine = Mock()
    mock_by_cuisine.return_value = [
        {'id': 1, 'title': 'abc', 'marketing_description': 'Our new recipe', 'otherField': 'ignore'},
        {'id': 2, 'title': 'foo', 'marketing_description': 'First recipe', 'otherField': 'ignore'},
        {'id': 99, 'title': 'bar', 'marketing_description': 'Another amazing recipe', 'otherField': 'ignore'},
        {'id': 10, 'title': 'baz1', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 11, 'title': 'baz2', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 12, 'title': 'baz3', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 13, 'title': 'baz4', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 14, 'title': 'baz5', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 15, 'title': 'baz6', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 16, 'title': 'baz7', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 17, 'title': 'baz8', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 18, 'title': 'baz9', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 19, 'title': 'baz10', 'marketing_description': 'more data', 'otherField': 'ignore'},
        {'id': 20, 'title': 'baz11', 'marketing_description': 'more data', 'otherField': 'ignore'},
    ]
    with patch('recipes.RecipeDAO.by_cuisine', mock_by_cuisine):
        context.response = context.client.get('/by-cuisine/british?start=2')
        mock_by_cuisine.assert_called_once_with('british')


@then(u'I can see a list of recipes')
def step_impl(context):
    data = context.response.get_json()
    assert data == {
        'start': 2,
        'limit': 10,
        'count': 14,
        'recipes': [
            {'id': 2, 'title': 'foo', 'marketing_description': 'First recipe'},
            {'id': 99, 'title': 'bar', 'marketing_description': 'Another amazing recipe'},
            {'id': 10, 'title': 'baz1', 'marketing_description': 'more data'},
            {'id': 11, 'title': 'baz2', 'marketing_description': 'more data'},
            {'id': 12, 'title': 'baz3', 'marketing_description': 'more data'},
            {'id': 13, 'title': 'baz4', 'marketing_description': 'more data'},
            {'id': 14, 'title': 'baz5', 'marketing_description': 'more data'},
            {'id': 15, 'title': 'baz6', 'marketing_description': 'more data'},
            {'id': 16, 'title': 'baz7', 'marketing_description': 'more data'},
            {'id': 17, 'title': 'baz8', 'marketing_description': 'more data'},
        ]
    }, data


@then(u'the list is split into paginated results with 10 recipes per page')
def step_impl(context):
    data = context.response.get_json()
    assert data['limit'] == 10
    assert len(data['recipes']) == 10


@then(u'each recipe has to contain only the fields ID, title and description')
def step_impl(context):
    data = context.response.get_json()
    for recipe in data['recipes']:
        assert list(recipe.keys()) == ['id', 'title', 'marketing_description']


@when(u'I update one or more recipes fields')
def step_impl(context):
    data = {
        'title': 'New recipe title',
        'marketing_description': 'New description',
    }
    context.response = context.client.put('/recipes/1', data=json.dumps(data), content_type='application/json')


@then(u'I can see the updated recipe fields')
def step_impl(context):
    data = context.response.get_json()
    assert data['title'] == 'New recipe title'
    assert data['marketing_description'] == 'New description'

    recipe = DAO.get(1)
    assert recipe['title'] == 'New recipe title'
    assert recipe['marketing_description'] == 'New description'
