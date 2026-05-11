from .repositories import UserRepository


class UserService:

    @staticmethod
    def register(username: str, password: str):
        return UserRepository.create_user(
            username=username,
            password=password,
        )