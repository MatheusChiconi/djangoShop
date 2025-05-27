from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def login_user(request):
    email = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'contas/login.html', {'email': email})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'contas/login.html', {'email': email})
    
    context = {
        'email': email,
    }
    return render(request, 'contas/login.html', context)

def register_user(request):
    return render(request, 'contas/register.html')