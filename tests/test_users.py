from http import HTTPStatus


def test_create_user(client, user_data):
    response = client.post("/users", json=user_data.model_dump(mode="json"))
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data["email"] == user_data.email
    assert data["username"] == user_data.username
    assert "id" in data
    assert data["id"] is not None
    assert "created_at" in data
    assert data["created_at"] is not None
    assert "password" not in data
    assert "hashed_password" not in data


def test_duplicated_username(client, user_data):
    client.post("/users", json=user_data.model_dump(mode="json"))
    response = client.post(
        "/users",
        json={
            "username": user_data.username,
            "email": "different@email.com",
            "password": user_data.password,
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Username already exists"


def test_duplicated_email(client, user_data):
    client.post("/users", json=user_data.model_dump(mode="json"))
    response = client.post(
        "/users",
        json={
            "username": "differentusername",
            "email": user_data.email,
            "password": user_data.password,
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Email already exists"


def test_users_me_unauthorized(client):
    response = client.get("/users/me")
    data = response.json()
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert data["detail"] == "Not authenticated"


def test_patch_user_username(client, test_user, headers):
    response = client.patch("/users/me", headers=headers, json={"username": "NewMaria"})

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["username"] == "NewMaria"
    assert data["email"] == test_user.email


def test_patch_user_email(client, test_user, headers):
    response = client.patch(
        "/users/me", headers=headers, json={"email": "newmaria@email.com"}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["email"] == "newmaria@email.com"
    assert data["username"] == test_user.username


def test_patch_user_password(client, test_user, headers):
    response = client.patch(
        "/users/me", headers=headers, json={"password": "newsecret123"}
    )

    assert response.status_code == HTTPStatus.OK

    login_response = client.post(
        "/auth/token", data={"username": test_user.email, "password": "newsecret123"}
    )

    login_data = login_response.json()

    assert login_response.status_code == HTTPStatus.OK
    assert "access_token" in login_data


def test_patch_duplicated_username(client, test_user, headers, other_user_data):
    client.post("/users", json=other_user_data.model_dump(mode="json"))

    response = client.patch(
        "/users/me", headers=headers, json={"username": other_user_data.username}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Username already exists"


def test_patch_duplicated_email(client, test_user, headers, other_user_data):
    client.post("/users", json=other_user_data.model_dump(mode="json"))

    response = client.patch(
        "/users/me", headers=headers, json={"email": other_user_data.email}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Email already exists"


def test_delete_me(client, headers):
    response = client.delete("/users/me", headers=headers)

    assert response.status_code == HTTPStatus.NO_CONTENT

    get_response = client.get("/users/me", headers=headers)

    assert get_response.status_code == HTTPStatus.UNAUTHORIZED
