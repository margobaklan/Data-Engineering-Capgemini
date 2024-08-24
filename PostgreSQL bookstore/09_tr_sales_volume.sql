-- a trigger that automatically increases the price of a book by 10% if the total quantity sold
-- reaches a certain threshold. This helps to dynamically adjust pricing based on the popularity of the book.

CREATE OR REPLACE FUNCTION adjust_book_price()
RETURNS TRIGGER
LANGUAGE plpgsql
AS 
$$
DECLARE
    total_quantity INTEGER;
    current_price NUMERIC(10, 2);
    new_price NUMERIC(10, 2);
BEGIN
    SELECT COALESCE(SUM(quantity), 0)
    INTO total_quantity
    FROM Sales
    WHERE book_id = NEW.book_id;
    
    IF total_quantity >= 5 THEN
        SELECT price
        INTO current_price
        FROM Books
        WHERE book_id = NEW.book_id;

        new_price := current_price * 1.10;

        UPDATE Books
        SET price = new_price
        WHERE book_id = NEW.book_id;
    END IF;
    
    RETURN NEW; 
END;
$$;

CREATE TRIGGER tr_adjust_book_price
AFTER INSERT ON Sales
FOR EACH ROW
EXECUTE FUNCTION adjust_book_price();

