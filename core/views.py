from django.shortcuts import render
from produtos.models import Produto

def home(request):
    produtos = Produto.objects.filter(
        estoque__gt=0
    ).only('id', 'nome', 'marca', 'preco', 'imagem_principal')[:16]
    
    context = {
        'produtos': produtos
    }
    
    return render(request, 'core/home.html', context)