from http import HTTPStatus


def test_create_novelist_name_sanitization(client,headers):
    response = client.post(
        '/novelists',
        headers=headers,
        json = {
            'name':'ClAriCe    LisPecTor    '
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'clarice lispector'

def test_novelist_update_name_sanitization(client,headers,test_novelist):
    response = client.patch(
        f'/novelists/{test_novelist.id}',
        headers = headers,
        json={
            'name':'ClAriCe    LisPecTor    '
        }
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['name'] == 'clarice lispector'

def test_book_update_title_sanitization(client,test_book,headers):
    response = client.patch(
        f'/books/{test_book.id}',
        headers = headers,
        json={
        'title':'a HorA dA EstRelA    '
        }
        )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data['title'] == 'a hora da estrela'

def test_create_book_title_sanitization(client, headers, test_novelist):
    response = client.post(
        '/books/',
        headers=headers,
        json={
            'title': 'a HorA dA EstRelA    ',
            'year': 1999,
            'novelist_id': test_novelist.id
        },
    )
    data = response.json()
    assert data['title'] == 'a hora da estrela'
    assert response.status_code == HTTPStatus.OK