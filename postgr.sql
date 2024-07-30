CREATE TABLE table1 (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    value VARCHAR(255)
);

-- Create a stored procedure to insert a new item into table1
CREATE OR REPLACE FUNCTION insert_item(name VARCHAR, value VARCHAR)
RETURNS VOID AS $$
BEGIN
    INSERT INTO table1 (name, value) VALUES (name, value);
END;	
$$ LANGUAGE plpgsql;

-- Create or replace a procedure that either inserts or updates a record
CREATE OR REPLACE FUNCTION add_or_update_item(p_id INTEGER, p_name VARCHAR, p_value VARCHAR)
RETURNS VOID AS $$
BEGIN
    -- Update if record exists
    UPDATE table1
    SET name = p_name, value = p_value
    WHERE id = p_id;
    
    -- Insert if record does not exist
    IF NOT FOUND THEN
        INSERT INTO table1 (id, name, value) VALUES (p_id, p_name, p_value);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create or replace procedure to delete an item by ID
CREATE OR REPLACE FUNCTION delete_item(p_id INTEGER)
RETURNS VOID AS $$
BEGIN
    DELETE FROM table1 WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

-- Create or replace procedure to update an item by ID
CREATE OR REPLACE FUNCTION update_item(p_id INTEGER, p_name VARCHAR, p_value VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE table1
    SET name = p_name, value = p_value
    WHERE id = p_id;
    
    -- If no row was updated, raise an exception
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item with ID % does not exist', p_id;
    END IF;
END;
$$ LANGUAGE plpgsql;


-- Create or replace procedure to retrieve an item by ID
CREATE OR REPLACE FUNCTION get_item(p_id INTEGER)
RETURNS TABLE(id INTEGER, name VARCHAR, value VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT table1.id, table1.name, table1.value
    FROM table1
    WHERE table1.id = p_id;
END;
$$ LANGUAGE plpgsql;


select * from table1