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
                defaults={'quantity': qnt, 'price': product.preco, 'marca': product.marca, 'old_price': product.comparacao_preco if product.tem_desconto() else None})
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
                    'marca': product.marca
                }
            else:
                self.cart[product_id]['quantity'] += qnt
            self.save()

    def remove(self, productId):

        product_id = str(productId)

        if self.user.is_authenticated:
            # Remove from DB cart for authenticated users
            try:
                # Get the product object first (since CartItem has a ForeignKey to Product)
                product_obj = Produto.objects.get(id=product_id)
                # Then find and delete the cart item
                item = CartItem.objects.get(cart=self.db_cart, product=product_obj)
                item.delete()
            except (Produto.DoesNotExist, CartItem.DoesNotExist):
                pass
        else:
            if product_id in self.cart:
                del self.cart[product_id]
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
                    'product_id': item.product.id,
                })
            return db_items
        else:
            result = []
            for product_id, item_data in self.cart.items():
                item_copy = item_data.copy()
                item_copy['product_id'] = product_id
                result.append(item_copy)
            return result

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
        
    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)

        if self.user.is_authenticated:
            # Update quantity in DB cart for authenticated users
            try:
                item = CartItem.objects.get(cart=self.db_cart, product__id=product_id)
                item.quantity = quantity
                print(f"Updating quantity for {item.product.nome} to {quantity}")
                item.save()
            except CartItem.DoesNotExist:
                pass
        else:
            # Update quantity in session cart for anonymous users
            if product_id in self.cart:
                self.cart[product_id]['quantity'] = quantity
                self.save()
