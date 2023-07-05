import './Banner.css'

function Banner(){
    return (<div class="banner">
    <div class="news">
      <div class="news-item active">
        <img src="caminho-da-imagem-da-noticia" alt="Imagem da Notícia" />
        <h2>Título da Notícia</h2>
        <p>Conteúdo da Notícia</p>
      </div>
      <div class="news-item">
        <img src="caminho-da-imagem-da-noticia" alt="Imagem da Notícia" />
        <h2>Título da Notícia</h2>
        <p>Conteúdo da Notícia</p>
      </div>
      <div class="news-item">
        <img src="caminho-da-imagem-da-noticia" alt="Imagem da Notícia" />
        <h2>Título da Notícia</h2>
        <p>Conteúdo da Notícia</p>
      </div>
      <div class="news-item">
        <img src="caminho-da-imagem-da-noticia" alt="Imagem da Notícia" />
        <h2>Título da Notícia</h2>
        <p>Conteúdo da Notícia</p>
      </div>
      <div class="news-item">
        <img src="caminho-da-imagem-da-noticia" alt="Imagem da Notícia" />
        <h2>Título da Notícia</h2>
        <p>Conteúdo da Notícia</p>
      </div>
      <div class="news-indicator">
        <span class="current">•</span>
        <span class="other">•</span>
        <span class="other">•</span>
        <span class="other">•</span>
        <span class="other">•</span>
      </div>
      <div class="arrow arrow-left">&lt;</div>
      <div class="arrow arrow-right">&gt;</div>
    </div>
  </div>)
}

export default Banner