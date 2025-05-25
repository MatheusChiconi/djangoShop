from django.shortcuts import render, get_object_or_404
from .models import Produto

def produtos(request, codigo):
    produto = get_object_or_404(Produto, codigo=codigo)
    todos_produtos = Produto.objects.filter(
        estoque__gt=0
    ).exclude(
        codigo=produto.codigo
    ).order_by('?').only('id', 'nome', 'marca', 'preco', 'imagem_principal')[:4]

    context = {
        'produto': produto,
        'todos_produtos': todos_produtos,
    }

    return render(request, 'produtos/sproduct.html', context)