import React, { useState } from "react";
import axios from "axios";
import "./BookItem.css";

function BookItem({ ulrImg, titulo, avaliacao, autor, sinopse, slug }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isCommenting, setIsCommenting] = useState(false);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");

  const handleItemClick = () => {
    if (isExpanded) {
      setIsExpanded(false);
      setIsCommenting(false);
    } else {
      setIsExpanded(true);
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

  //API
  const handleSendEvaluation = () => {
    const data = { rating, comment };
    axios
      .post("/api/avaliacao", data)
      .then((response) => {})
      .catch((error) => {});

    console.log("Avaliação enviada:", { rating, comment });
  };

  return (
    <div className="book-item" >
      <div className="book-info" onClick={handleItemClick}>
        <img src={ulrImg} alt="Capa do Livro"  />
        <div className="book-details">
          <div className="title">{titulo}</div>
          <div className="rating">&#9733;&#9733;&#9733;&#9734;&#9734;</div>
          <div>
            {autor}
          </div>
        </div>
      </div>

      {isExpanded && (
        <div className="expanded-content">
          <div className="sinopse-section">
            <h2>Sinopse</h2>
            <p>{sinopse}</p>
          </div>

          {!isCommenting && (
            <div className="actions">
              <button onClick={handleEvaluateButtonClick}>Avaliar</button>
            </div>
          )}

          {isCommenting && (
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
                  placeholder="Escreva sua avaliação..."
                  value={comment}
                  onChange={handleCommentChange}
                ></textarea>
              </div>
              <button onClick={handleSendEvaluation}>Enviar</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default BookItem;
