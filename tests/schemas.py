from madr_api.schemas import UserPublic


class TestUser(UserPublic):
    clear_password: str

