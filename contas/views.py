import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserUpdateForm

User = get_user_model()

def validar_cpf(cpf: str) -> bool:
    if not cpf:
        return False 

    cpf = re.sub(r'[^0-9]', '', cpf) 

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = ((soma * 10) % 11) % 10
    if digito1 != int(cpf[9]):
        return False

    # Segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = ((soma * 10) % 11) % 10
    if digito2 != int(cpf[10]):
        return False

    return True

def login_user(request):
    email_do_formulario = ""
    if request.method == 'POST':
        email_do_formulario = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email_do_formulario)
            username_para_autenticar = user_obj.username 
        except User.DoesNotExist:
            messages.error(request, 'Email ou senha inválidos.')
            return render(request, 'contas/login.html', {'email': email_do_formulario})

        user = authenticate(request, username=username_para_autenticar, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos.')
            return render(request, 'contas/login.html', {'email': email_do_formulario})

    context = {
        'email': email_do_formulario, 
    }
    return render(request, 'contas/login.html', context)

def register_user(request):
    nome_form = ""
    email_form = ""
    telefone_form = ""
    cpf_form = ""

    if request.method == 'POST':
        nome_form = request.POST.get('nome', '').strip()
        email_form = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        telefone_form = request.POST.get('telefone', '').strip()
        cpf_form = request.POST.get('cpf', '').strip()

        erros = False
        if cpf_form and not validar_cpf(cpf_form):
            messages.error(request, 'CPF inválido. Por favor, insira um CPF válido.')
            erros = True

        if not nome_form or not email_form or not password1 or not password2:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios (Nome, Email, Senhas).')
            erros = True
        
        if password1 != password2:
            messages.error(request, 'As senhas não coincidem.')
            erros = True
        
        if User.objects.filter(email=email_form).exists():
            messages.error(request, 'Já existe um usuário cadastrado com este email.')
            erros = True

        if cpf_form and User.objects.filter(cpf=cpf_form).exists():
            messages.error(request, 'Já existe um usuário cadastrado com este CPF.')
            erros = True

        if not erros:
            username_gerado = email_form.split('@')[0]
            if User.objects.filter(username=username_gerado).exists():
                base_username = username_gerado
                contador = 1
                while User.objects.filter(username=username_gerado).exists():
                    username_gerado = f"{base_username}{contador}"
                    contador += 1
            
            try:
                user = User.objects.create_user(
                    username=username_gerado, 
                    email=email_form, 
                    password=password1, 
                    first_name=nome_form,
                    telefone=telefone_form if telefone_form else None,
                    cpf=cpf_form
                )
                messages.success(request, 'Cadastro realizado com sucesso! Agora você pode fazer login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f"Ocorreu um erro inesperado durante o cadastro: {e}")

    context = {
        'nome': nome_form,
        'email': email_form,
        'telefone': telefone_form,
        'cpf': cpf_form,
    }
    return render(request, 'contas/register.html', context)

@login_required
def account(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações atualizadas com sucesso!')
            return redirect('account')  # ou 'contas:account' se estiver com namespace
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'contas/account-page.html', {
        'form': form,
        'user': user
    })
