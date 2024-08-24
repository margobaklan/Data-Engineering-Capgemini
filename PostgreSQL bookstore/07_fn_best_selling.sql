-- a function that returns the top N best-selling books in a specific genre, based on total sales revenue.

CREATE OR REPLACE FUNCTION fn_get_top_n_books_by_genre(
    p_genre_id INTEGER,
    p_top_n INTEGER
)
RETURNS TABLE (
    book_title VARCHAR(255),
    total_revenue NUMERIC(10, 2)
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        b.title AS book_title,
        SUM(s.quantity * b.price) AS total_revenue
    FROM
        Books b
    JOIN
        Sales s ON b.book_id = s.book_id
    WHERE
        b.genre_id = p_genre_id
    GROUP BY
        b.book_id
    ORDER BY
        total_revenue DESC
    LIMIT
        p_top_n;
END;
$$;

-- This would return the top 5 best-selling books in genre with ID 17
SELECT * FROM fn_get_top_n_books_by_genre(17, 5);

