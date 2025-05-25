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