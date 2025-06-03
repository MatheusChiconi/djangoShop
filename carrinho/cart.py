class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get the current session key if it exists
        cart = self.session.get('session_key')
        # If the user is new, no session key! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} # Tudo que está no carrinho

        # Make sure cart is available on all pages of site
        self.cart = cart

    def add(self, product, qnt=1):
        # Add a product to the cart
        if str(product.id) not in self.cart:
            # Fica um dicionario de produtos com o id do produto como chave
            # {'id1': {'quantity': 0, 'price': float(price)}, 'id2': {'quantity': 0, 'price': float(price)}}
            self.cart[int(product.id)] = {
                'quantity': qnt,
                'price': float(product.preco),
                'old_price': (
                    float(product.comparacao_preco)
                    if product.tem_desconto()
                    else None
                ),
                'image': product.imagem_principal.url,
            }
        self.cart[int(product.id)]['quantity'] += qnt
        # Save the session with the updated cart
        self.save()

    def save(self):
        self.session['session_key'] = self.cart
        self.session.modified = True
    
    def get_total_price(self):
        return sum(item['quantity'] * item['price'] for item in self.cart.values())

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())

    def items(self):
        """Retorna os itens do carrinho"""
        return self.cart.values()