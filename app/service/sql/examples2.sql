CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.examples2 (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(32) NOT NULL, 
    age SMALLINT NOT NULL
);

DO
$do$
BEGIN
    IF (SELECT COUNT(*) FROM dev.examples2) = 0 THEN
        INSERT INTO dev.examples2 (name, age) VALUES 
            ('Alice', 25),
            ('Bob', 30),
            ('Charlie', 35);
    END IF;
END
$do$;