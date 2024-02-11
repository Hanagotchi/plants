#!/bin/bash

set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "plants" <<-'EOSQL'
    CREATE SCHEMA IF NOT EXISTS dev;
    CREATE TABLE 
        IF NOT EXISTS dev.plants (
            id SERIAL PRIMARY KEY, 
            id_user INT NOT NULL,
            name VARCHAR(64) NOT NULL, 
            scientific_name VARCHAR(64) NOT NULL
    );

    DO $do$ BEGIN
        IF (SELECT COUNT(*) FROM dev.plants) = 0 THEN
            INSERT INTO dev.plants (id_user, name, scientific_name) VALUES 
                (1, 'Rosa', 'Rosa'),
                (2, 'Margarita', 'Margarita'),
                (3, 'Girasol', 'Girasol');
        END IF;
    END $do$;
EOSQL
