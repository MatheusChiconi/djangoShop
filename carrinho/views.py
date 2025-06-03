from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from produtos.models import Produto
from .cart import Cart

@require_POST
def add_to_cart(request, product_id, qnt=1):
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=product_id)
    if produto.estoque < qnt:
        # Se o estoque for menor que a quantidade, não adiciona ao carrinho
        return redirect('home')
    cart.add(produto, qnt=qnt)
    code = produto.codigo
    return redirect(f'/produto/{code}/')
