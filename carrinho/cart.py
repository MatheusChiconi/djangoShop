from .models import Cart as CartDB, CartItem
from produtos.models import Produto

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        
        # For authenticated users, use DB cart
        if self.user.is_authenticated:
            self.db_cart, _ = CartDB.objects.get_or_create(user=self.user)
            # Initialize session cart but don't use it for authenticated users
            self.cart = self.session.get('session_key', {})
        else:
            # For anonymous users, use session cart
            cart = self.session.get('session_key')
            if 'session_key' not in request.session:
                cart = self.session['session_key'] = {}
            self.cart = cart

    def add(self, product, qnt=1):
        product_id = str(product.id)

        if self.user.is_authenticated:
            # Use DB cart for authenticated users
            item, created = CartItem.objects.get_or_create(
                cart=self.db_cart,
                product=product,
                defaults={'quantity': qnt, 'price': product.preco, 'old_price': product.comparacao_preco if product.tem_desconto() else None}
            )
            if not created:
                item.quantity += qnt
                item.save()
        else:
            # Use session cart for anonymous users
            if product_id not in self.cart:
                self.cart[product_id] = {
                    'quantity': qnt,
                    'price': float(product.preco),
                    'old_price': float(product.comparacao_preco) if product.tem_desconto() else None,
                    'image': product.imagem_principal.url,
                    'name': product.nome,
                }
            else:
                self.cart[product_id]['quantity'] += qnt
            self.save()

    def items(self):
        """Return cart items regardless of storage method"""
        if self.user.is_authenticated:
            # Return items from DB for authenticated users
            db_items = []
            for item in self.db_cart.items.all():
                db_items.append({
                    'quantity': item.quantity,
                    'price': float(item.price),
                    'old_price': float(item.old_price) if item.old_price else None,
                    'image': item.product.imagem_principal.url,
                    'name': item.product.nome,
                })
            return db_items
        else:
            # Return session items for anonymous users
            return self.cart.values()

    def save(self):
        self.session['session_key'] = self.cart
        self.session.modified = True
    
    def get_total_price(self):
        if self.user.is_authenticated:
            # Calculate from database items
            return sum(item.quantity * float(item.price) for item in self.db_cart.items.all())
        else:
            # Calculate from session items
            return sum(item['quantity'] * item['price'] for item in self.cart.values())
    
    def get_total_old_price(self):
        if self.user.is_authenticated:
            # Calculate from database items
            return sum(item.quantity * float(item.old_price) for item in self.db_cart.items.all() if item.old_price)
        else:
            # Calculate from session items
            return sum(item['quantity'] * item['old_price'] for item in self.cart.values() if item['old_price'])

    def get_total_quantity(self):
        if self.user.is_authenticated:
            # Calculate from database items
            return sum(item.quantity for item in self.db_cart.items.all())
        else:
            # Calculate from session items
            return sum(item['quantity'] for item in self.cart.values())
