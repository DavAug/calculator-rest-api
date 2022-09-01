import json

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
    response = client.post('/calc', json={"expression": "-1 * (2 * 6 / 3)"})
    data = json.loads(response.data)

    assert data == 1
