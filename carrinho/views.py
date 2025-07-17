from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
import json
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

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@require_POST
@csrf_protect
def remove_from_cart(request, product_id=None):
    cart = Cart(request)
    
    if product_id is not None:
        # URL parameter case
        try:
            cart.remove(int(product_id))
            return HttpResponse(status=204)
        except (ValueError, TypeError):
            return HttpResponse(status=400)
    else:
        # JSON data case
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            if not product_id:
                return JsonResponse({'status': 'error'}, status=400)
            
            cart.remove(int(product_id))

            response_data = {
                'status': 'success',
                'new_price': cart.get_total_price(),
                'new_price_without_discount': cart.get_total_old_price(),
            }

            return JsonResponse(response_data, status=200)

        except (json.JSONDecodeError, ValueError, TypeError):
            return JsonResponse({'status': 'error'}, status=400)
        except Exception:
            return JsonResponse({'status': 'error'}, status=500) 


def cart_detail(request):
    cart = Cart(request)
    
    return render(request, 'carrinho/cart_detail.html', {'cart': cart})

@csrf_protect
def update_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        cart = Cart(request)
        cart.update_quantity(product_id, quantity)

        response_data = {
                'status': 'success',
                'new_price': cart.get_total_price(),
                'new_price_without_discount': cart.get_total_old_price(),
            }

        return JsonResponse(response_data, status=200)

    return JsonResponse({'status': 'error'}, status=400)