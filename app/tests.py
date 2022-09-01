import pytest

from .__init__ import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    response = client.get("/")
    assert b"Welcome to the calculator API!" in response.data


def test_calculator(client):
    # Check response is correct
    response = client.post('/calc', json={"expression": "0.3"})
    assert response.json["result"] == "0.3"

    response = client.post('/calc', json={"expression": "0.3 + 1 + 2"})
    assert response.json["result"] == "3.3"

    response = client.post('/calc', json={"expression": "-1 * (2 * 6 / 3)"})
    assert response.json["result"] == "-4"

    # Error is thrown when no data is posted
    response = client.post('/calc')
    assert response.status == '400 BAD REQUEST'

    # Error is thrown when JSON does not have "expression" property
    response = client.post('/calc', json={"wrong": "format"})
    assert response.status == '400 BAD REQUEST'

    # Error is thrown when JSON's expression field does not have the correct
    # type
    response = client.post('/calc', json={"expression": 123})
    assert response.status == '400 BAD REQUEST'
