const mainImg = document.getElementById("mainImg");
const smallImgs = document.getElementsByClassName("small-img");

if (mainImg) {
    for (const oneSmallImg of smallImgs) {
        oneSmallImg.addEventListener("click", function() {
            mainImg.src = oneSmallImg.src;
        });
    }
} else {
    console.warn("A imagem principal com ID 'mainImg' não foi encontrada. A funcionalidade de clique não será ativada.");
}



document.addEventListener('DOMContentLoaded', function() {
    // Get the notification and close button
    const notification = document.getElementById('cart-notification');
    const closeBtn = document.querySelector('.notification-close');
    
    // Add close button functionality
    if (closeBtn && notification) {
        closeBtn.addEventListener('click', function() {
            notification.classList.remove('show');
        });
    }
    
    // Auto-hide after 4 seconds
    if (notification && notification.classList.contains('show')) {
        setTimeout(function() {
            notification.classList.remove('show');
        }, 4000);
    }
});

// Add to cart button animation
document.addEventListener('DOMContentLoaded', function() {
    const addToCartForm = document.getElementById('add-to-cart-form');
    const addToCartButton = addToCartForm?.querySelector('button');
    
    if (addToCartForm && addToCartButton) {
        addToCartForm.addEventListener('submit', function(e) {
            // Add animation class to button
            addToCartButton.classList.add('adding-to-cart');
            
            // Create shine effect
            const btnShine = addToCartButton.querySelector('.btn-shine');
            if (!btnShine) {
                const shine = document.createElement('span');
                shine.classList.add('btn-shine');
                addToCartButton.appendChild(shine);
            }
            
            // Trigger shine animation
            setTimeout(() => {
                const shine = addToCartButton.querySelector('.btn-shine::after');
                if (shine) {
                    shine.style.opacity = '1';
                    shine.style.transition = 'transform 0.8s, opacity 0.8s';
                    shine.style.transform = 'rotate(45deg) translateX(150%)';
                    
                    setTimeout(() => {
                        shine.style.opacity = '0';
                    }, 600);
                }
            }, 100);
            
            // Change button text
            const originalText = addToCartButton.textContent;
            addToCartButton.textContent = 'Adicionando...';
            
            // Small delay to let animation play before actual submission
            setTimeout(() => {
                addToCartButton.classList.remove('adding-to-cart');
                addToCartButton.textContent = originalText;
            }, 1000);
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const quantityInput = document.querySelector('input[name="quantity"]');
    const maxStock = parseInt(quantityInput.getAttribute('max'));
    
    // Update maximum value in real-time
    quantityInput.addEventListener('change', function() {
        // Ensure value is at least 1
        if (this.value < 1) {
            this.value = 1;
        }
        
        // Ensure value doesn't exceed stock
        if (this.value > maxStock) {
            this.value = maxStock;
            alert(`Apenas ${maxStock} itens disponíveis em estoque.`);
        }
    });
});

