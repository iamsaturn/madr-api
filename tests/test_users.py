from http import HTTPStatus

import pytest

from tests.schemas import TestUser
def test_create_user(client, user_data):
    response = client.post(
        '/users',
        json= user_data.model_dump(mode='json'))
    assert response.status_code == HTTPStatus.OK

def test_duplicated_username(client, user_data):
    client.post(
        '/users', json = user_data.model_dump(mode='json')
    )
    response = client.post(
        '/users', json = {'username': user_data.username,
                         'email': 'different@email.com',
                         'password': user_data.password}
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Username already exists'

def test_duplicated_email(client, user_data):
    client.post(
        '/users', json = user_data.model_dump(mode='json')
    )
    response = client.post(
        '/users', json = {'username': 'differentusername',
                         'email': user_data.email,
                         'password': user_data.password}
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Email already exists'

def test_users_me_unauthorized(client):
    response = client.get('/users/me')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Not authenticated'
    


