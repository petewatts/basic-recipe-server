from app import app
from behave import fixture, use_fixture


@fixture
def test_client(context, *args, **kwargs):
    app.testing = True
    context.client = app.test_client()
    yield context.client


def before_feature(context, feature):
    use_fixture(test_client, context)
