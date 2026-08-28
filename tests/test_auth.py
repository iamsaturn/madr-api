from http import HTTPStatus

from madr_api.security import create_access_token


def test_me_with_valid_token(client,test_user, headers):
    response = client.get(
        '/users/me',
        headers= headers
    )
    data = response.json()
    assert data['username'] == test_user.username
    assert data['email'] == test_user.email
    assert response.status_code == HTTPStatus.OK


def test_with_wrong_password(client,test_user):
    response = client.post(
        '/auth/token',
        data = {
            'username': test_user.email,
            'password':'itsawrongpassword'
        }
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'

def test_login_with_nonexistent_email(client):
    response = client.post(
        '/auth/token',
        data={
            'username': "inexistent@email.com",
            'password': "abcdef1*gh"
        }
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'

def test_protected_route_with_invalid_token(client):
    response = client.get(
        '/users/me',
        headers = {
            'Authorization': 'Bearer invalid-token'
        }
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] =='Could not validate credentials'

def test_token_without_user_in_database(client):
    token = create_access_token({'sub':'nonexistent@email.com'})
    response = client.get(
        '/users/me',
        headers= {'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'

def test_token_without_sub(client):
    token = create_access_token({})
    response = client.get(
        '/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Could not validate credentials'
