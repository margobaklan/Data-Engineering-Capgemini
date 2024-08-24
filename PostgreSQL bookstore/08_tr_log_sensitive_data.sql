-- a trigger that logs any changes made to sensitive data in a Customers table. Sensitive data:
-- first name, last name, email address. The trigger inserts a record into an audit log table. 

CREATE TABLE CustomersLog (
    log_id SERIAL PRIMARY KEY,
    column_name VARCHAR(50),
    old_value TEXT,
    new_value TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(50) 
);

CREATE OR REPLACE FUNCTION log_sensitive_data_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS 
$$
BEGIN
    IF NEW.first_name IS DISTINCT FROM OLD.first_name THEN
        INSERT INTO CustomersLog(column_name, old_value, new_value, changed_by)
        VALUES('first_name', OLD.first_name, NEW.first_name, current_user);
    END IF;

    IF NEW.last_name IS DISTINCT FROM OLD.last_name THEN
        INSERT INTO CustomersLog(column_name, old_value, new_value, changed_by)
        VALUES('last_name', OLD.last_name, NEW.last_name, current_user);
    END IF;

    IF NEW.email IS DISTINCT FROM OLD.email THEN
        INSERT INTO CustomersLog(column_name, old_value, new_value, changed_by)
        VALUES('email', OLD.email, NEW.email, current_user);
    END IF;

    RETURN NEW;
END;
$$;

CREATE TRIGGER tr_log_sensitive_data_changes
AFTER UPDATE ON Customers
FOR EACH ROW
EXECUTE FUNCTION log_sensitive_data_changes();

