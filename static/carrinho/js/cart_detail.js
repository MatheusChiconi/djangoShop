document.addEventListener('DOMContentLoaded', () => {
    
    // --- REMOÇÃO COM ANIMAÇÃO ---
    document.querySelectorAll('.remove-btn').forEach(button => {
        button.addEventListener('click', () => {
            const cardToRemove = button.closest('.product-card');

            // Adiciona a classe que ativa a animação CSS
            cardToRemove.classList.add('removing');

            // Aguarda a animação terminar antes de remover o item do DOM
            cardToRemove.addEventListener('animationend', () => {
                cardToRemove.remove();
            });
        });
    });

});
