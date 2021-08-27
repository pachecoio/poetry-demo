from api import __version__


def test_version():
    assert __version__ == "0.1.0"


class TestUser:
    BASE_URL = "/api/user"

    def test_get_users(self, app, client):
        resp = client.get(self.BASE_URL)
        assert resp.status_code == 200
        assert len(resp.json["data"]) == 0

    def test_create_users(self, app, client):
        user_data = dict(
            name="Jon Snow",
            email="jon@winterfell.com",
            password="Igritte"
        )
        resp = client.post(self.BASE_URL, json=user_data)
        assert resp.status_code == 201
        data = resp.json["data"]

        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]