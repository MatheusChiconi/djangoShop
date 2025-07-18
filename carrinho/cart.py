# carrinho/cart.py

from .models import Cart as CartDB, CartItem
from produtos.models import Produto

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        
        # Para usuários autenticados, usa o carrinho do banco de dados
        if self.user.is_authenticated:
            self.db_cart, _ = CartDB.objects.get_or_create(user=self.user)
            self.cart = self.session.get('session_key', {}) # A sessão é apenas um backup
        else:
            # Para anônimos, usa o carrinho da sessão
            cart = self.session.get('session_key')
            if 'session_key' not in request.session:
                cart = self.session['session_key'] = {}
            self.cart = cart

    def add(self, product, qnt=1):
        product_id = str(product.id)

        if self.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(
                cart=self.db_cart,
                product=product,
                defaults={'quantity': qnt}
            )
            if not created:
                item.quantity += qnt
                item.save()
        else:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': qnt}
            else:
                self.cart[product_id]['quantity'] += qnt
            self.save()

    def remove(self, productId):
        product_id = str(productId)
        if self.user.is_authenticated:
            try:
                product_obj = Produto.objects.get(id=product_id)
                item = CartItem.objects.get(cart=self.db_cart, product=product_obj)
                item.delete()
            except (Produto.DoesNotExist, CartItem.DoesNotExist):
                pass
        else:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if self.user.is_authenticated:
            try:
                item = CartItem.objects.get(cart=self.db_cart, product__id=product_id)
                item.quantity = quantity
                item.save()
            except CartItem.DoesNotExist:
                pass
        else:
            if product_id in self.cart:
                self.cart[product_id]['quantity'] = quantity
                self.save()

    def items(self):
        if self.user.is_authenticated:
            cart_items = self.db_cart.items.select_related('product')
            db_items = []
            for item in cart_items:
                db_items.append({
                    'quantity': item.quantity,
                    'price': float(item.product.preco),
                    'old_price': float(item.product.comparacao_preco) if item.product.tem_desconto() else None,
                    'image': item.product.imagem_principal.url,
                    'name': item.product.nome,
                    'marca': item.product.marca,
                    'product_id': item.product.id,
                })
            return db_items
        else:
            product_ids = self.cart.keys()
            products = Produto.objects.filter(id__in=product_ids)
            result = []
            for product in products:
                product_id_str = str(product.id)
                result.append({
                    'quantity': self.cart[product_id_str]['quantity'],
                    'price': float(product.preco),
                    'old_price': float(product.comparacao_preco) if product.tem_desconto() else None,
                    'image': product.imagem_principal.url,
                    'name': product.nome,
                    'marca': product.marca,
                    'product_id': product.id,
                })
            return result

    def save(self):
        self.session['session_key'] = self.cart
        self.session.modified = True
    
    def get_total_price(self):
        if self.user.is_authenticated:
            return sum(item.quantity * item.product.preco for item in self.db_cart.items.select_related('product'))
        else:
            product_ids = self.cart.keys()
            products = Produto.objects.filter(id__in=product_ids)
            return sum(self.cart[str(p.id)]['quantity'] * p.preco for p in products)
    
    def get_total_old_price(self):
        if self.user.is_authenticated:
            return sum(item.quantity * item.product.comparacao_preco for item in self.db_cart.items.select_related('product') if item.product.tem_desconto())
        else:
            product_ids = self.cart.keys()
            products = Produto.objects.filter(id__in=product_ids)
            return sum(self.cart[str(p.id)]['quantity'] * p.comparacao_preco for p in products if p.tem_desconto())

    def get_total_quantity(self):
        if self.user.is_authenticated:
            return sum(item.quantity for item in self.db_cart.items.all())
        else:
            return sum(item['quantity'] for item in self.cart.values())