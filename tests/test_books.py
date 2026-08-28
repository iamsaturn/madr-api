from http import HTTPStatus


def test_post_book(client,book_data, headers):
    response = client.post(
        '/books',
        headers=headers,
        json= {
            'title': book_data.title,
            'year': book_data.year,
            'novelist_id': book_data.novelist_id
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['title'] == book_data.title
    assert data['year'] == book_data.year
    assert data['novelist']['id'] == book_data.novelist_id
    assert 'id' in data

def test_post_inexistent_novelist(client,book_data,headers):
    response = client.post(
        '/books',
        headers=headers,
        json={
            'title': book_data.title,
            'year': book_data.year,
            'novelist_id': 999

        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data['detail'] == 'Novelist not found'

def test_get_book_list(client, test_book):
    response = client.get(
        '/books'
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert isinstance(data, list)
    assert data[0]['title'] == test_book.title
    assert data[0]['year'] == test_book.year
    assert data[0]['id'] == test_book.id
    

def test_get_book_by_id(client,test_book):
    response = client.get(
        f'/books/{test_book.id}'
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert isinstance(data, dict)
    assert data['id'] == test_book.id
    assert data['title'] == test_book.title
    assert data['novelist']['id'] == test_book.novelist.id

def test_get_nonexistent_book_by_id(client):
    response = client.get(
        '/books/999'
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data['detail'] == 'Book not found'

def test_patch_book(client,test_book,headers, test_other_novelist):
    response = client.patch(
        f'/books/{test_book.id}',
        headers=headers,
        json={
            'title': 'Newtitle',
            'year': 2010,
            'novelist_id': test_other_novelist.id
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['title'] == 'newtitle'
    assert data['year'] == 2010
    assert data['novelist'] == test_other_novelist.model_dump(mode='json')
    assert isinstance(data,dict)

def test_patch_inexistent_book(client,headers,test_novelist):
    response = client.patch(
        '/books/999',
        headers=headers,
        json={
            'title':'validtitle',
            'year':0,
            'novelist_id':test_novelist.id
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data['detail'] == 'Book not found'

def test_patch_book_inexistent_author(client,test_book,headers):
    response = client.patch(
        f'/books/{test_book.id}',
        headers=headers,
        json={
            'title':'Newtitle',
            'year':2010,
            'novelist_id':999
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data['detail'] == 'Novelist not found'

def test_delete_book(client,test_book,headers):
    response = client.delete(
        f'/books/{test_book.id}',
        headers=headers
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
    get_response = client.get(
        f'/books/{test_book.id}',
        headers=headers
    )
    get_data = get_response.json()
    assert get_response.status_code == HTTPStatus.NOT_FOUND
    assert get_data['detail'] == 'Book not found'

def test_delete_nonexistent_book(client, headers):
    response = client.delete(
        '/books/999',
        headers=headers
    )
    data = response.json()
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data['detail'] == 'Book not found'
