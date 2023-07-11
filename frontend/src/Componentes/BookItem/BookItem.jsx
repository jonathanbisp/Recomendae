import React, { useState } from "react";
import axios from "axios";
import "./BookItem.css";

function BookItem({ user, ulrImg, titulo, autor, sinopse }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isCommenting, setIsCommenting] = useState(false);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");
  const [reviews, setReviews] = useState([]);

  const handleItemClick = () => {
    if (isExpanded) {
      setIsExpanded(false);
      setIsCommenting(false);
    } else {
      setIsExpanded(true);
      setIsCommenting(false);
    }
  };

  const handleRatingChange = (value) => {
    setRating(value);
  };

  const handleCommentChange = (event) => {
    setComment(event.target.value);
  };

  const handleEvaluateButtonClick = () => {
    setIsCommenting(true);
  };

  const handleSendEvaluation = () => {
    if (rating === 0) {
      alert("Por favor, dê uma avaliação em estrelas.");
      return;
    }

    const newReview = {
      usuario: user || "Anônimo",
      data: getCurrentDate(),
      avaliacao: rating,
      comentario: comment || "",
    };

    setReviews([newReview, ...reviews]);

    setRating(0);
    setComment("");
    setIsCommenting(false);
  };

  const getCurrentDate = () => {
    const now = new Date();
    const day = String(now.getDate()).padStart(2, "0");
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const year = now.getFullYear();
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="book-item">
      <div className="book-info" onClick={handleItemClick}>
        <div className="book-cover">
          <img src={ulrImg} alt="Capa do Livro" />
        </div>
        <div className="book-details">
          <div className="title">{titulo}</div>
          <div className="rating">&#9733;&#9733;&#9733;&#9734;&#9734;</div>
          <div>{user || "Anônimo"}</div>
        </div>
      </div>

      {isExpanded && (
        <div className="expanded-content">
          <div className="sinopse-section">
            <h2>Sinopse</h2>
            <p className="sinopse-text">{sinopse}</p>
          </div>

          {!isCommenting ? (
            <div className="actions">
              <button onClick={handleEvaluateButtonClick}>Avaliar</button>
            </div>
          ) : (
            <div className="comment-section">
              <div className="rating-section">
                <p>Avaliação:</p>
                {[1, 2, 3, 4, 5].map((value) => (
                  <span
                    key={value}
                    className={`star ${rating >= value ? "active" : ""}`}
                    onClick={() => handleRatingChange(value)}
                  >
                    &#9733;
                  </span>
                ))}
              </div>
              <div className="comment-textarea">
                <textarea
                  placeholder="Escreva sua avaliação (opcional)..."
                  value={comment}
                  onChange={handleCommentChange}
                ></textarea>
              </div>
              <button onClick={handleSendEvaluation}>Enviar</button>
            </div>
          )}

          <div className="reviews-section">
            <h2>Avaliações</h2>
            <div className="reviews-content">
              {reviews.length > 0 ? (
                reviews
                  .sort((a, b) => new Date(a.data) - new Date(b.data))
                  .map((review, index) => (
                    <div key={index} className="review">
                      <div className="review-info">
                        <div className="review-user">{review.usuario}</div>
                        <div className="review-date">{review.data}</div>
                        <div className="review-rating">
                          {Array.from({ length: review.avaliacao }).map((_, index) => (
                            <span key={index}>&#9733;</span>
                          ))}
                        </div>
                      </div>
                      {review.comentario && (
                        <div className="review-comment">{review.comentario}</div>
                      )}
                    </div>
                  ))
              ) : (
                <div>Nenhuma avaliação disponível.</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BookItem;
