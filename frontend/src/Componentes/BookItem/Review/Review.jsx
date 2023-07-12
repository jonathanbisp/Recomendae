import { useState } from "react";

function Review(){
    const [reviews, setReview] = useState([])

    return (
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
    )
}

export default Review;