-- a stored procedure that updates the join_date of each customer to the date of their first
-- purchase if it is earlier than the current join_date. This ensures that the join_date reflects the true
-- start of the customer relationship.

create or replace PROCEDURE sp_update_customer_join_date()
LANGUAGE plpgsql
AS 
$$
BEGIN
    UPDATE Customers c
    SET join_date = subquery.first_purchase_date
    FROM (
        SELECT
            customer_id,
            MIN(sale_date) AS first_purchase_date
        FROM
            Sales
        GROUP BY
            customer_id
    ) AS subquery
    WHERE
        c.customer_id = subquery.customer_id
        AND subquery.first_purchase_date < c.join_date;
END;
$$;