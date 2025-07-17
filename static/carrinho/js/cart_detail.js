const DELAY = 300; // Tempo em milissegundos para debounce

function debounce(func) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, DELAY);
    };
}

function updateCartSummary(newTotal, newSubtotal) {
    // Atualiza os valores de subtotal e total no DOM
    const subtotalEl = document.getElementById('subtotal');
    const totalEl = document.getElementById('total');

    const totalValue = typeof newTotal === 'number' ? newTotal : 0;
    const subtotalValue = typeof newSubtotal === 'number' ? newSubtotal : 0;

    const formatCurrency = (value) => value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

    subtotalEl.textContent = formatCurrency(subtotalValue);
    totalEl.textContent = formatCurrency(totalValue);
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', () => 
        {
            const divProduct = button.closest('.card-body');
            const productId = divProduct.getAttribute('data-id');

            const jsonData = { 'product_id': productId };
            console.log(jsonData);

            $.ajax({
                url: '/carrinho/remove-from-cart/',
                type: 'POST',
                data: JSON.stringify(jsonData),
                contentType: 'application/json',
                headers: { 'X-CSRFToken': CSRF_TOKEN },
                success: function(response) {
                    const cardToRemove = button.closest('.product-card');
                    const new_price = response.new_price;
                    const new_price_without_discount = response.new_price_without_discount

                    cardToRemove.classList.add('removing');
                    cardToRemove.addEventListener('animationend', () => {
                        cardToRemove.remove();
                    });

                    updateCartSummary(new_price, new_price_without_discount);
                },
                error: function(xhr, status, error) {
                    console.error('Erro ao remover o item:', error);
                }
            });
        });
    });
});

function sendQuantityUpdate(itemId, newQuantity, input) {
    // Debug: Enviando ao servidor -> Produto: ${itemId}, Quantidade: ${newQuantity}
    $.ajax({
        url: '/carrinho/update-quantity/',
        type: 'POST',
        data: JSON.stringify({ product_id: itemId, quantity: newQuantity }),
        contentType: 'application/json',
        headers: { 'X-CSRFToken': CSRF_TOKEN },
        success: function(response) {
            const new_price = response.new_price;
            const new_price_without_discount = response.new_price_without_discount

            input.value = newQuantity;
            updateCartSummary(new_price, new_price_without_discount);
        },
        error: function(xhr, status, error) {
            console.error('Erro ao atualizar a quantidade:', error);
        }
    });
}

const debouncedUpdateQuantity = debounce(sendQuantityUpdate);

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".quantity-btn");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const change = parseInt(this.dataset.change);
            const container = this.closest(".d-flex");
            const input = container.querySelector(".quantity-input");
            const cardBody = this.closest(".card-body");
            const itemId = cardBody.dataset.id;
            let currentQuantity = parseInt(input.value);
            const newQuantity = currentQuantity + change;

            if (newQuantity >= 1) {
                input.value = newQuantity;
                debouncedUpdateQuantity(itemId, newQuantity, input);
            }
        });
    });
});