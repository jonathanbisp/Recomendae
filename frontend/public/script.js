// Variáveis para controlar o banner de notícias
let currentNewsIndex = 0;
const newsItems = document.querySelectorAll('.news-item');
const newsIndicator = document.querySelector('.news-indicator');
const arrowLeft = document.querySelector('.arrow-left');
const arrowRight = document.querySelector('.arrow-right');

// Função para mostrar a próxima notícia
function showNextNews() {
  newsItems[currentNewsIndex].classList.remove('active');
  currentNewsIndex = (currentNewsIndex + 1) % newsItems.length;
  newsItems[currentNewsIndex].classList.add('active');
  updateNewsIndicator();
}

// Função para mostrar a notícia anterior
function showPreviousNews() {
  newsItems[currentNewsIndex].classList.remove('active');
  currentNewsIndex = (currentNewsIndex - 1 + newsItems.length) % newsItems.length;
  newsItems[currentNewsIndex].classList.add('active');
  updateNewsIndicator();
}

// Função para atualizar o indicador de notícias
function updateNewsIndicator() {
  newsIndicator.textContent = '.'.repeat(currentNewsIndex) + ' ' + '.'.repeat(newsItems.length - currentNewsIndex - 1);
}

// Função para avançar para a próxima notícia automaticamente a cada 5 segundos
function autoNextNews() {
  setInterval(showNextNews, 5000);
}

// Event listeners para as setas do banner de notícias
arrowLeft.addEventListener('click', showPreviousNews);
arrowRight.addEventListener('click', showNextNews);

// Inicialização do banner de notícias
if (newsItems.length > 0) {
  updateNewsIndicator();
  newsItems[currentNewsIndex].classList.add('active');

  // Chamada da função para iniciar a rotação automática das notícias
  autoNextNews();
}

//Menu lateral

// Seleciona o ícone do menu
const menuIcon = document.querySelector('.menu-icon');
// Seleciona o menu
const menu = document.querySelector('.menu');

// Adiciona um ouvinte de evento de clique ao ícone do menu
menuIcon.addEventListener('click', toggleMenu);

// Alterna a classe 'active' no menu ao clicar no ícone do menu
function toggleMenu() {
  menu.classList.toggle('active');
}

// Seleciona o ícone de fechar
const closeIcon = document.querySelector('.close-icon');

// Adiciona um ouvinte de evento de clique ao ícone de fechar
closeIcon.addEventListener('click', closeMenu);

// Função para fechar o menu
function closeMenu() {
  menu.classList.remove('active');
}

// Adiciona um ouvinte de evento de clique no documento inteiro
document.addEventListener('click', function(event) {
  var targetElement = event.target;

  // Verifica se o clique foi fora da barra lateral ou do ícone do menu
  if (!menu.contains(targetElement) && !menuIcon.contains(targetElement)) {
    menu.classList.remove('active');
  }
});
