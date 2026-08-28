from http import HTTPStatus


def test_post_book(client, book_data, headers):

    response = client.post(
        "/books",
        headers=headers,
        json={
            "title": book_data.title,
            "year": book_data.year,
            "novelist_id": book_data.novelist_id,
        },
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data["title"] == book_data.title
    assert data["year"] == book_data.year
    assert data["novelist"]["id"] == book_data.novelist_id
    assert "id" in data


def test_post_already_created_book(client, test_book, headers, test_novelist):
    response = client.post(
        "/books",
        headers=headers,
        json={"title": test_book.title, "year": 1999, "novelist_id": test_novelist.id},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Book already exists"


def test_post_inexistent_novelist(client, book_data, headers):
    response = client.post(
        "/books",
        headers=headers,
        json={"title": book_data.title, "year": book_data.year, "novelist_id": 999},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Novelist not found"


def test_get_book_list(client, test_book):
    response = client.get("/books")
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert isinstance(data, list)
    assert data[0]["title"] == test_book.title
    assert data[0]["year"] == test_book.year
    assert data[0]["id"] == test_book.id


def test_get_book_by_id(client, test_book):

    response = client.get(f"/books/{test_book.id}")

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(data, dict)
    assert data["id"] == test_book.id
    assert data["title"] == test_book.title
    assert data["novelist"]["id"] == test_book.novelist.id


def test_get_nonexistent_book_by_id(client):
    response = client.get("/books/999")
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Book not found"


def test_patch_book(client, test_book, headers, test_other_novelist):
    response = client.patch(
        f"/books/{test_book.id}",
        headers=headers,
        json={"title": "Newtitle", "year": 2010, "novelist_id": test_other_novelist.id},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data["title"] == "newtitle"
    assert data["year"] == 2010
    assert data["novelist"] == test_other_novelist.model_dump(mode="json")
    assert isinstance(data, dict)


def test_patch_inexistent_book(client, headers, test_novelist):
    response = client.patch(
        "/books/999",
        headers=headers,
        json={"title": "validtitle", "year": 0, "novelist_id": test_novelist.id},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Book not found"


def test_patch_book_inexistent_author(client, test_book, headers):

    response = client.patch(
        f"/books/{test_book.id}",
        headers=headers,
        json={"title": "Newtitle", "year": 2010, "novelist_id": 999},
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Novelist not found"


def test_patch_book_overwrite(client, test_book, headers, test_novelist):

    post_response = client.post(
        "/books",
        headers=headers,
        json={
            "title": "the second book",
            "novelist_id": test_novelist.id,
            "year": 1999,
        },
    )
    post_data = post_response.json()
    response = client.patch(
        f"/books/{post_data['id']}", headers=headers, json={"title": test_book.title}
    )
    data = response.json()
    assert response.status_code == HTTPStatus.CONFLICT
    assert data["detail"] == "Book already exists"


def test_delete_book(client, test_book, headers):
    response = client.delete(f"/books/{test_book.id}", headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT
    get_response = client.get(f"/books/{test_book.id}", headers=headers)
    get_data = get_response.json()
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_data["detail"] == "Book not found"


def test_delete_nonexistent_book(client, headers):
    response = client.delete("/books/999", headers=headers)
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["detail"] == "Book not found"


def test_partial_search_book_by_title(client, test_book):
    response = client.get("/books", params={"title": test_book.title[:-2]})
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(data) == 1
    assert data[0]["id"] == test_book.id
    assert data[0]["title"] == test_book.title


def test_search_book_by_year(client, test_book):
    response = client.get("/books", params={"year": test_book.year})

    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert len(data) == 1
    assert data[0]["id"] == test_book.id
    assert data[0]["year"] == test_book.year


def test_limit_search_book(client, test_book, headers, test_novelist):
    client.post(
        "/books",
        headers=headers,
        json={"title": "second book", "year": 2000, "novelist_id": test_novelist.id},
    )

    response = client.get("/books", params={"limit": 1})

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(data) == 1


def test_offset_search_book(client, test_book, headers, test_novelist):
    second_response = client.post(
        "/books",
        headers=headers,
        json={"title": "second book", "year": 2000, "novelist_id": test_novelist.id},
    )

    second_book = second_response.json()

    response = client.get("/books", params={"offset": 1})

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(data) == 1
    assert data[0]["id"] == second_book["id"]


def test_search_book_by_title_and_year(client, test_book, headers, test_novelist):
    client.post(
        "/books",
        headers=headers,
        json={
            "title": "another star book",
            "year": 2005,
            "novelist_id": test_novelist.id,
        },
    )

    response = client.get(
        "/books", params={"title": test_book.title[:-2], "year": test_book.year}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(data) == 1
    assert data[0]["id"] == test_book.id
