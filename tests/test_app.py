from app import app


class TestApp(object):

    def test_app_has_debug_disabled(self):
        # Assert
        assert not app.debug

    def test_index(self, client):
        # Act
        response = client.get('/')
        # Assert
        assert response.status_code == 200

    def test_index_content(self, client):
        # Act
        response = client.get('/')
        # Assert
        assert b'swagger' in response.data
