-- a function that calculates the average price of books within a specific genre.

CREATE OR REPLACE FUNCTION fn_avg_price_by_genre(p_genre_id INTEGER)
RETURNS NUMERIC(10, 2)
LANGUAGE plpgsql
AS 
$$
DECLARE
    avg_price NUMERIC(10, 2);
BEGIN
    SELECT
        AVG(price)
    INTO
        avg_price
    FROM
        Books
    WHERE
        genre_id = p_genre_id;
    RETURN avg_price;
END;
$$;

-- This would return the average price of books in the genre with ID 6.
SELECT fn_avg_price_by_genre(6);

