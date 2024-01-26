import json, requests, schemas
import os

from jsonschema import validate

SCHEMA_INIT = os.path.abspath(schemas.__file__)  # происходит ссылка на __init__, который никуда не денется
SCHEMA_DIR = os.path.dirname(SCHEMA_INIT)


# 1. на каждый из методов GET/POST/PUT/DELETE ручек reqres.in
# 3. На разные статус-коды 200/201/204/404/400

def test_list_users_status_code():
    response = requests.get('https://reqres.in/api/users?page=2')
    assert response.status_code == 200


def test_create_user_status_code():
    response = requests.post('https://reqres.in/api/users', json={"name": "Vin", "job": "leader"})
    assert response.status_code == 201


def test_update_user_status_code():
    response = requests.patch('https://reqres.in/api/users/2', json={"name": "Vin", "job": "resident"})
    assert response.status_code == 200


def test_delete_user_status_code():
    response = requests.delete('https://reqres.in/api/users/2')
    assert response.status_code == 204


def test_registration_unsuccessful_status_code():
    response = requests.post('https://reqres.in/api/register', json={"email": "sydney@fife"})
    assert response.status_code == 400


def test_single_user_not_found_status_code():
    response = requests.get('https://reqres.in/api/users/23')
    assert response.status_code == 404


# 2. Позитивные/Негативные тесты на одну из ручек.
# 5. С ответом
def test_login_successful():
    response = requests.post('https://reqres.in/api/login',
                             json={"email": "eve.holt@reqres.in", "password": "cityslicka"})
    assert response.status_code == 200
    body = response.json()
    assert body['token'] == 'QpwL5tke4Pnpja7X4'


def test_login_fails_without_email_and_password():
    response = requests.post('https://reqres.in/api/login')
    assert response.status_code == 400
    body = response.json()
    assert body['error'] == 'Missing email or username'


# 5. и без ответа
def test_delete_user_check_empty_response():
    response = requests.delete('https://reqres.in/api/users/2')
    print(response.text)
    assert response.text == ''


def test_single_user_not_found_returns_empty_body():
    response = requests.get('https://reqres.in/api/users/23')
    assert response.status_code == 404
    body = response.json()
    assert body == {}


# На разные схемы (4-5 схем)

def test_list_users_validate_schema():
    response = requests.get('https://reqres.in/api/users?page=2')
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "get_users_list.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_single_user_validate_schema():
    response = requests.get('https://reqres.in/api/users/2')
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "single_user.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_create_user_validate_schema():
    response = requests.post('https://reqres.in/api/users/', json={"name": "morpheus", "job": "leader"})
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "create_user.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_register_user_validate_schema():
    response = requests.post('https://reqres.in/api/register',
                             json={"email": "eve.holt@reqres.in", "password": "pistol"})
    body = response.json()
    schema = os.path.join(SCHEMA_DIR, "registration.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


# 6. На бизнес-логику (заметить какую-то фичу и автоматизировать, как делали на уроке)
def test_if_username_and_job_updated():
    name = 'Ellend'
    job = 'Mistborn'
    response = requests.post('https://reqres.in/api/users', json={"name": name, "job": job})
    body = response.json()
    assert body["name"] == name
    assert body["job"] == job
