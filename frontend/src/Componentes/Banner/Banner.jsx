import React, { useState, useEffect } from 'react';
import './Banner.css';

function Banner() {
  const newsData = [
    {
      image: 'caminho-da-imagem-da-noticia-1',
      title: 'Título da Notícia 1',
      content: 'Conteúdo da Notícia 1',
    },
    {
      image: 'caminho-da-imagem-da-noticia-2',
      title: 'Título da Notícia 2',
      content: 'Conteúdo da Notícia 2',
    },
    {
      image: 'caminho-da-imagem-da-noticia-3',
      title: 'Título da Notícia 3',
      content: 'Conteúdo da Notícia 3',
    },
    {
      image: 'caminho-da-imagem-da-noticia-4',
      title: 'Título da Notícia 4',
      content: 'Conteúdo da Notícia 4',
    },
    {
      image: 'caminho-da-imagem-da-noticia-5',
      title: 'Título da Notícia 5',
      content: 'Conteúdo da Notícia 5',
    },
  ];

  const [currentNews, setCurrentNews] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentNews((prevNews) => (prevNews + 1) % newsData.length);
    }, 5000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  const handlePreviousNews = () => {
    setCurrentNews((prevNews) => (prevNews - 1 + newsData.length) % newsData.length);
  };

  const handleNextNews = () => {
    setCurrentNews((prevNews) => (prevNews + 1) % newsData.length);
  };

  return (
    <div className="banner">
      <div className="news">
        {newsData.map((news, index) => (
          <div key={index} className={`news-item ${currentNews === index ? 'active' : ''}`}>
            <img src={news.image} alt="Imagem da Notícia" />
            <h2>{news.title}</h2>
            <p>{news.content}</p>
          </div>
        ))}
        <div className="news-indicator">
          {newsData.map((_, index) => (
            <span
              key={index}
              className={`indicator-dot ${currentNews === index ? 'current' : ''}`}
            >
              •
            </span>
          ))}
        </div>
        <div className="arrow arrow-left" onClick={handlePreviousNews}>
          &lt;
        </div>
        <div className="arrow arrow-right" onClick={handleNextNews}>
          &gt;
        </div>
      </div>
    </div>
  );
}

export default Banner;
