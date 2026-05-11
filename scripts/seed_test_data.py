from apps.users.models import User


User.objects.create_user(
    username='admin',
    password='admin',
)