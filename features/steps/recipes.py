from behave import given, when, then
from app import DAO
from datetime import datetime


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


