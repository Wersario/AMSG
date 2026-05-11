from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from apps.users.services import UserService


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/api/history/1/')
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/chats/')
            return redirect(next_url)

        return render(request, 'users/login.html', {
            'error': 'Invalid username or password.',
        })


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect('/')


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/chats/')
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username or not password:
            return render(request, 'users/register.html', {
                'error': 'Заполните все поля.'
            })

        if password != password2:
            return render(request, 'users/register.html', {
                'error': 'Пароли не совпадают.',
                'username': username,
            })

        if len(password) < 6:
            return render(request, 'users/register.html', {
                'error': 'Пароль должен быть не менее 6 символов.',
                'username': username,
            })

        from django.contrib.auth import get_user_model
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {
                'error': 'Пользователь с таким именем уже существует.',
                'username': username,
            })

        user = UserService.register(username=username, password=password)
        login(request, user)
        return redirect('/chats/')
