from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('core:home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Валидация
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
        else:
            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('core:home')
    
    return render(request, 'accounts/register.html')

def guest_login(request):
    # Просто создаем гостевого пользователя
    guest_user, created = User.objects.get_or_create(
        username='guest',
        defaults={'is_active': True}
    )
    if created:
        guest_user.set_password('guest123')
        guest_user.save()
    
    login(request, guest_user)
    messages.info(request, 'Вы вошли как гость. Функционал ограничен.')
    return redirect('core:home')