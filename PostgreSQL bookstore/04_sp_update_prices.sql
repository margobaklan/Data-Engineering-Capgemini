-- a stored procedure that increases the prices of all books in a specific genre by a specified
-- percentage. The procedure also outputs the number of books that were updated.

CREATE OR REPLACE PROCEDURE sp_bulk_update_book_prices_by_genre(
    p_genre_id INTEGER,
    p_percentage_change NUMERIC(5, 2)
)
LANGUAGE plpgsql
AS 
$$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE Books
    SET price = price * (1 + p_percentage_change / 100)
    WHERE genre_id = p_genre_id;
    GET DIAGNOSTICS updated_count = ROW_COUNT;
    RAISE NOTICE 'Number of books updated: %', updated_count;
END;
$$;

-- This increases the prices of all books in genre ID 6 by 100% and output the updated number
CALL sp_bulk_update_book_prices_by_genre(6, 100.00);
