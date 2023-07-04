-- name: add-book-to-favorites!
INSERT INTO favorites (user_id, book_id)
VALUES ((SELECT id FROM users WHERE username = :username),
        (SELECT id FROM books WHERE slug = :slug))
ON CONFLICT DO NOTHING;


-- name: remove-book-from-favorites!
DELETE
FROM favorites
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND book_id = (SELECT id FROM books WHERE slug = :slug);


-- name: is-book-in-favorites^
SELECT CASE WHEN count(user_id) > 0 THEN TRUE ELSE FALSE END AS favorited
FROM favorites
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND book_id = (SELECT id FROM books WHERE slug = :slug);


-- name: get-favorites-count-for-book^
SELECT count(*) as favorites_count
FROM favorites
WHERE book_id = (SELECT id FROM books WHERE slug = :slug);


-- name: get-tags-for-book-by-slug
SELECT t.tag
FROM tags t
         INNER JOIN books_to_tags att ON
        t.tag = att.tag
        AND
        att.book_id = (SELECT id FROM books WHERE slug = :slug);


-- name: get-book-by-slug^
SELECT id,
       slug,
       title,
       description,
       body,
       created_at,
       updated_at,
       (SELECT username FROM users WHERE id = author_id) AS author_username
FROM books
WHERE slug = :slug
LIMIT 1;


-- name: create-new-book<!
WITH author_subquery AS (
    SELECT id, username
    FROM users
    WHERE username = :author_username
)
INSERT
INTO books (slug, title, description, body, author_id)
VALUES (:slug, :title, :description, :body, (SELECT id FROM author_subquery))
RETURNING
    id,
    slug,
    title,
    description,
    body,
        (SELECT username FROM author_subquery) as author_username,
    created_at,
    updated_at;


-- name: add-tags-to-book*!
INSERT INTO books_to_tags (book_id, tag)
VALUES ((SELECT id FROM books WHERE slug = :slug),
        (SELECT tag FROM tags WHERE tag = :tag))
ON CONFLICT DO NOTHING;


-- name: update-book<!
UPDATE books
SET slug        = :new_slug,
    title       = :new_title,
    body        = :new_body,
    description = :new_description
WHERE slug = :slug
  AND author_id = (SELECT id FROM users WHERE username = :author_username)
RETURNING updated_at;


-- name: delete-book!
DELETE
FROM books
WHERE slug = :slug
  AND author_id = (SELECT id FROM users WHERE username = :author_username);


-- name: get-books-for-feed
SELECT a.id,
       a.slug,
       a.title,
       a.description,
       a.body,
       a.created_at,
       a.updated_at,
       (
           SELECT username
           FROM users
           WHERE id = a.author_id
       ) AS author_username
FROM books a
         INNER JOIN followers_to_followings f ON
        f.following_id = a.author_id AND
        f.follower_id = (SELECT id FROM users WHERE username = :follower_username)
ORDER BY a.created_at
LIMIT :limit
OFFSET
:offset;

-- name: add-rating-to-book!
INSERT INTO ratings (user_id, book_id, rating)
VALUES ((SELECT id FROM users WHERE username = :username),
        (SELECT id FROM books WHERE slug = :slug),
        :rating)
ON CONFLICT (user_id, book_id) DO UPDATE
SET rating = EXCLUDED.rating;

-- name: update-rating-for-book!
UPDATE ratings
SET rating = :new_rating
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND book_id = (SELECT id FROM books WHERE slug = :slug);

-- name: get-average-rating-for-book
SELECT AVG(rating) AS average_rating
FROM ratings
WHERE book_id = (SELECT id FROM books WHERE slug = :slug);

-- name: is-book-rated-by-user^
SELECT CASE WHEN count(user_id) > 0 THEN TRUE ELSE FALSE END AS rated
FROM ratings
WHERE user_id = (SELECT id FROM users WHERE username = :username)
  AND book_id = (SELECT id FROM books WHERE slug = :slug);