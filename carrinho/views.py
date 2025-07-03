from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from produtos.models import Produto
from .cart import Cart
from django.contrib import messages


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=product_id)
    
    # Get quantity from form data, default to 1 if not provided
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    
    # Check stock
    if produto.estoque < quantity:
        messages.error(request, f"Estoque insuficiente para {produto.nome}.")
        return redirect('home')
    
    cart.add(produto, qnt=quantity)
    
    # Add success message
    messages.success(request, f"{produto.nome} foi adicionado ao carrinho!")
    
    code = produto.codigo
    return redirect(f'/produto/{code}/')

@require_POST
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    
    return HttpResponse(status=204)

def cart_detail(request):
    cart = Cart(request)
    
    return render(request, 'carrinho/cart_detail.html', {'cart': cart})