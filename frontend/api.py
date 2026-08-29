import requests

API_URL = "https://madr-api.fly.dev"


def login(email, password):
    data = {
        "username": email,
        "password": password,
    }

    response = requests.post(f"{API_URL}/auth/token", data=data)
    return response


def register(username, email, password):
    data = {
        "username": username,
        "email": email,
        "password": password,
    }

    response = requests.post(f"{API_URL}/users/", json=data)
    return response


def get_profile(token):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.get(f"{API_URL}/users/me", headers=headers)
    return response


def get_books(offset=0, limit=6):
    params = {
        "offset": offset,
        "limit": limit,
    }

    response = requests.get(f"{API_URL}/books/", params=params)
    return response


def create_book(title, year, novelist_id, token):
    data = {
        "title": title,
        "year": year,
        "novelist_id": novelist_id,
    }

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{API_URL}/books/",
        json=data,
        headers=headers,
    )
    return response


def get_novelists(offset=0, limit=6):
    params = {
        "offset": offset,
        "limit": limit,
    }

    response = requests.get(f"{API_URL}/novelists/", params=params)
    return response


def create_novelist(name, token):
    data = {
        "name": name,
    }

    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(
        f"{API_URL}/novelists/",
        json=data,
        headers=headers,
    )
    return response
