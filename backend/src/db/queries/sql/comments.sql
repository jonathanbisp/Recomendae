-- name: get-reviews-for-book-by-slug
SELECT c.id,
       c.comment,
       c.rating,
       c.created_at,
       c.updated_at,
       (SELECT username FROM users WHERE id = c.author_id) as author_username
FROM reviews c
         INNER JOIN books a ON c.book_id = a.id AND (a.slug = :slug);

-- name: get-review-by-id-and-slug^
SELECT c.id,
       c.comment,
       c.rating,
       c.created_at,
       c.updated_at,
       (SELECT username FROM users WHERE id = c.author_id) as author_username
FROM reviews c
         INNER JOIN books a ON c.book_id = a.id AND (a.slug = :book_slug)
WHERE c.id = :review_id;

-- name: create-new-review<!
WITH users_subquery AS (
        (SELECT id, username FROM users WHERE username = :author_username)
)
INSERT
INTO reviews (comment,rating, author_id, book_id)
VALUES (:comment,
        :rating,
        (SELECT id FROM users_subquery),
        (SELECT id FROM books WHERE slug = :book_slug))
RETURNING
    id,
    comment,
    rating,
        (SELECT username FROM users_subquery) AS author_username,
    created_at,
    updated_at;

-- name: delete-review-by-id!
DELETE
FROM reviews
WHERE id = :review_id
  AND author_id = (SELECT id FROM users WHERE username = :author_username);
