from http import HTTPStatus

def test_create_user(client, user_data):
    response = client.post(
        '/users',
        json= user_data.model_dump(mode='json'))
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['email'] == user_data.email
    assert data['username'] == user_data.username
    assert "id" in data
    assert data['id'] is not None
    assert "created_at" in data
    assert data['created_at'] is not None
    assert "password" not in data
    assert "hashed_password" not in data

def test_duplicated_username(client, user_data):
    client.post(
        '/users', json = user_data.model_dump(mode='json')
    )
    response = client.post(
        '/users', json = {'username': user_data.username,
                         'email': 'different@email.com',
                         'password': user_data.password}
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data['detail'] == 'Username already exists'

def test_duplicated_email(client, user_data):
    client.post(
        '/users', json = user_data.model_dump(mode='json')
    )
    response = client.post(
        '/users', json = {'username': 'differentusername',
                         'email': user_data.email,
                         'password': user_data.password}
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data['detail'] == 'Email already exists'

def test_users_me_unauthorized(client):
    response = client.get('/users/me')
    data = response.json()
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data['detail'] == 'Not authenticated'
    


