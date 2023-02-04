from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect


def index(request):
    """Функция выводит главную страницу"""
    return render(request, 'main/base.html', {'title': 'Главная страница'})


class LoginUser(LoginView):
    """Класс, реализующий вход пользователя"""
    form_model = AuthenticationForm
    template_name = 'main/login.html'


def logout_user(request):
    """Функция осуществляет выход пользователя из системы"""
    logout(request)
    return redirect('home')
