// Script for navigation bar
const bar = document.getElementById('bar');
const navbar = document.getElementById('navbar');
const close = document.getElementById('close');

// Verifica se a variável 'bar' está definida e não é nula ou falsa
if (bar) {
  // Adiciona um ouvinte de evento de clique ao elemento 'bar'
    bar.addEventListener('click', () => {
    // Adiciona a classe 'active' ao elemento 'nav' quando 'bar' é clicado
        navbar.classList.add('active');
  });
}
if (close) {
  close.addEventListener('click', () => {
    navbar.classList.remove('active');
  });
}

document.addEventListener('DOMContentLoaded', function() {
    // Find all cart item remove forms
    const removeForms = document.querySelectorAll('.remove-form');
    
    // Add event listener to each form
    removeForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Prevent normal form submission
            e.preventDefault();
            
            // Get the cart item element
            const cartItem = this.closest('.cart-item');
            
            // Get ONLY the pricing summary (not the button)
            const pricingSummary = document.querySelector('.cart-pricing-summary');
            
            // Send AJAX request
            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
                    // Add animation styles to the cart item
                    cartItem.style.transition = 'all 0.5s ease';
                    cartItem.style.opacity = '0';
                    cartItem.style.maxHeight = '0';
                    cartItem.style.margin = '0';
                    cartItem.style.padding = '0';
                    cartItem.style.overflow = 'hidden';
                    
                    // Hide ONLY the pricing summary with animation
                    if (pricingSummary) {
                        pricingSummary.style.transition = 'all 0.5s ease';
                        pricingSummary.style.opacity = '0';
                        pricingSummary.style.maxHeight = '0';
                        pricingSummary.style.overflow = 'hidden';
                        pricingSummary.style.margin = '0';
                        pricingSummary.style.padding = '0';
                    }
                    
                    // Actually remove the item after animation completes
                    setTimeout(() => {
                        cartItem.remove();
                        
                        // Check if cart is now empty
                        const remainingItems = document.querySelectorAll('.cart-item');
                        if (remainingItems.length === 0) {
                            // Show empty cart message
                            const cartItemsContainer = document.querySelector('.cart-items');
                            if (cartItemsContainer) {
                                const emptyMessage = document.createElement('p');
                                emptyMessage.textContent = 'Seu carrinho está vazio.';
                                emptyMessage.style.opacity = '0';
                                cartItemsContainer.innerHTML = '';
                                cartItemsContainer.appendChild(emptyMessage);
                                
                                // Fade in message
                                setTimeout(() => {
                                    emptyMessage.style.transition = 'opacity 0.3s ease';
                                    emptyMessage.style.opacity = '1';
                                }, 10);
                            }
                        }
                    }, 500);
                }
            })
            .catch(error => {
                console.error('Error removing cart item:', error);
            });
        });
    });
});