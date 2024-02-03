CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.examples1 (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(32) NOT NULL, 
    age SMALLINT NOT NULL
);

DO
$do$
BEGIN
    IF (SELECT COUNT(*) FROM dev.examples1) = 0 THEN
        INSERT INTO dev.examples1 (name, age) VALUES 
            ('John Doe', 30),
            ('Jane Doe', 28),
            ('Vincent Vega', 35),
            ('Mia Wallace', 32),
            ('Jules Winnfield', 33);
    END IF;
END
$do$;