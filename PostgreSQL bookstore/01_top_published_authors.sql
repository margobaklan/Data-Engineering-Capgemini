-- a CTE that calculates the total number of books each author has published.
-- SELECT query retrieve a list of authors who have published more than 3
-- books, including the number of books they have published.

WITH auth_total_books AS (
    SELECT
        aut.author_id,
        aut.name AS author_name,
        COUNT(b.book_id) AS total_books
    FROM
        authors aut
    LEFT JOIN
        books b ON aut.author_id = b.author_id
    GROUP BY
        aut.author_id, aut.name
)
SELECT
    author_name,
    total_books
FROM
    auth_total_books
WHERE
    total_books > 3;


