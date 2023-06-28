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

// Event listeners para as setas do banner de notícias
arrowLeft.addEventListener('click', showPreviousNews);
arrowRight.addEventListener('click', showNextNews);

// Inicialização do banner de notícias
updateNewsIndicator();
newsItems[currentNewsIndex].classList.add('active');

// Função para exibir a próxima notícia
function nextNews() {
  const activeNews = document.querySelector('.news-item.active');
  const nextNews = activeNews.nextElementSibling;
  
  if (nextNews !== null) {
    activeNews.classList.remove('active');
    nextNews.classList.add('active');
  }
}

// Função para exibir a notícia anterior
function prevNews() {
  const activeNews = document.querySelector('.news-item.active');
  const prevNews = activeNews.previousElementSibling;
  
  if (prevNews !== null) {
    activeNews.classList.remove('active');
    prevNews.classList.add('active');
  }
}

// Evento de clique na seta para a próxima notícia
const nextArrow = document.querySelector('.arrow-right');
nextArrow.addEventListener('click', nextNews);

// Evento de clique na seta para a notícia anterior
const prevArrow = document.querySelector('.arrow-left');
prevArrow.addEventListener('click', prevNews);


// Variável para controlar o estado do menu
let isMenuOpen = false;

// Função para alternar a exibição do menu
function toggleMenu() {
  const menuButton = document.querySelector('.menu-button');
  const menu = document.querySelector('.menu');

  isMenuOpen = !isMenuOpen;

  if (isMenuOpen) {
    menuButton.classList.add('active');
    menu.style.display = 'block';
  } else {
    menuButton.classList.remove('active');
    menu.style.display = 'none';
  }
}

// Event listener para o botão do menu
const menuButton = document.querySelector('.menu-button');
menuButton.addEventListener('click', toggleMenu);
