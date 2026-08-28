from madr_api.schemas import UserPublic


class CreatedUser(UserPublic):
    clear_password: str

