from .models import User


class UserRepository:

    @staticmethod
    def create_user(username: str, password: str):
        return User.objects.create_user(
            username=username,
            password=password,
        )

    @staticmethod
    def get_by_id(user_id: int):
        return User.objects.get(id=user_id)