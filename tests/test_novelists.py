from http import HTTPStatus


def test_create_novelist(client, novelist_data, headers):
    response = client.post(
        "/novelists", json=novelist_data.model_dump(mode="json"), headers=headers
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert "id" in data
    assert data["id"] is not None
    assert data["name"] == novelist_data.name


def test_create_already_existing_novelist(client, test_novelist, headers):
    response = client.post(
        "/novelists/", headers=headers, json={"name": test_novelist.name}
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Novelist already exists"


def test_get_novelists(client, test_novelist):
    response = client.get("/novelists")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert isinstance(data, list)
    assert data[0]["id"] == test_novelist.id
    assert data[0]["name"] == test_novelist.name


def test_get_novelist_by_id(client, test_novelist):
    response = client.get(f"/novelists/{test_novelist.id}")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert isinstance(data, dict)
    assert data["id"] == test_novelist.id
    assert data["name"] == test_novelist.name


def test_get_nonexistent_novelist(client):
    response = client.get("/novelists/999")
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Novelist not found"


def test_patch_novelist(client, test_novelist, headers):
    response = client.patch(
        f"/novelists/{test_novelist.id}", json={"name": "NewName"}, headers=headers
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data["name"] == "newname"
    assert data["id"] == test_novelist.id


def test_patch_nonexistent_novelist(client, headers):
    response = client.patch("/novelists/999", json={"name": "newname"}, headers=headers)
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Novelist not found"


def test_patch_novelist_overwrite(client, test_novelist, headers):
    post_response = client.post(
        "/novelists",
        headers=headers,
        json={
            "name": "Second Novelist",
        },
    )
    post_data = post_response.json()
    response = client.patch(
        f"/novelists/{post_data['id']}",
        headers=headers,
        json={"name": test_novelist.name},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Novelist already exists"


def test_delete_novelist(client, test_novelist, headers):
    response = client.delete(f"/novelists/{test_novelist.id}", headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT
    get_response = client.get(f"/novelists/{test_novelist.id}", headers=headers)
    get_data = get_response.json()
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_data["detail"] == "Novelist not found"


def test_delete_nonexistent_novelist(client, headers):
    response = client.delete("/novelists/999", headers=headers)
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Novelist not found"


def test_partial_search_novelist(client, test_novelist, test_other_novelist):

    response = client.get("/novelists", params={"name": test_novelist.name[:-2]})
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_novelist.name
    assert response.status_code == HTTPStatus.OK


def test_limit_search_novelist(client, test_novelist, test_other_novelist):
    response = client.get("/novelists", params={"limit": 1})
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data) == 1


def test_offset_novelist(client, test_novelist, test_other_novelist):
    response = client.get("/novelists", params={"offset": 1})
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_other_novelist.id
    assert response.status_code == HTTPStatus.OK
