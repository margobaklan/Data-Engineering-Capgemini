-- a stored procedure that uses a cursor to iterate over sales records older than a specific
-- date, moving them to SalesArchive table, and deletes them from the original Sales table.

CREATE TABLE SalesArchive (
    sale_id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL
);

CREATE OR REPLACE PROCEDURE sp_archive_old_sales(p_cutoff_date DATE)
LANGUAGE plpgsql
AS 
$$
DECLARE
    cur CURSOR FOR
        SELECT * FROM Sales
        WHERE sale_date < p_cutoff_date;
    rec Sales%ROWTYPE;
BEGIN
    OPEN cur;    
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;    
        INSERT INTO SalesArchive (sale_id, book_id, customer_id, quantity, sale_date)
        VALUES (rec.sale_id, rec.book_id, rec.customer_id, rec.quantity, rec.sale_date);        
        DELETE FROM Sales
        WHERE sale_id = rec.sale_id;
    END LOOP;    
    CLOSE cur;    
END;
$$;

CALL sp_archive_old_sales('2022-02-10');
