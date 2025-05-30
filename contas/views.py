from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

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
    nome = ""
    email = ""
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Validação simples
        if not nome or not email or not password1 or not password2:
            messages.error(request, 'Preencha todos os campos.')
        elif password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Já existe um usuário com este email.')
        else:
            username = email.split('@')[0]
            if User.objects.filter(username=username).exists():
                # Garante username único
                base_username = username
                count = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{count}"
                    count += 1
            user = User.objects.create_user(username=username, email=email, password=password1, first_name=nome)
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça login.')
            return redirect('login')

    context = {
        'nome': nome,
        'email': email,
    }
    return render(request, 'contas/register.html', context)

@login_required # Se não estiver logado, redireciona para a página de login
def account(request):
    context = {
        'user': request.user,
    }
    return render(request, 'contas/account-page.html', context)