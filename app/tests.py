import os
import pytest

from .__init__ import create_app


@pytest.fixture()
def app():
    app = create_app(testing=True)

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
    # Check history is initially empty
    response = client.get('/history')
    assert response.json == []

    # Check response is correct
    response = client.post('/calc', json={"expression": "0.3"})
    assert response.json["result"] == "0.3"
    response = client.get('/history')
    assert response.json[0] == {'id': 1, 'expression': '0.3', 'result': '0.3'}

    response = client.post('/calc', json={"expression": "0.3 + 1 + 2"})
    assert response.json["result"] == "3.3"
    response = client.get('/history')
    assert response.json[0] == {
        'id': 2, 'expression': '0.3 + 1 + 2', 'result': '3.3'}
    assert response.json[1] == {'id': 1, 'expression': '0.3', 'result': '0.3'}

    response = client.post('/calc', json={"expression": "-1 * (2 * 6 / 3)"})
    assert response.json["result"] == "-4"
    response = client.get('/history')
    assert response.json[0] == {
        'id': 3, 'expression': '-1 * (2 * 6 / 3)', 'result': '-4'}
    assert response.json[1] == {
        'id': 2, 'expression': '0.3 + 1 + 2', 'result': '3.3'}
    assert response.json[2] == {'id': 1, 'expression': '0.3', 'result': '0.3'}

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


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Delete test database, once tests are run."""
    def remove_test_db():
        os.remove('test.db')
    request.addfinalizer(remove_test_db)
