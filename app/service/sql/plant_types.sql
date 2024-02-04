CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.plant_types (
    botanical_name VARCHAR(70) PRIMARY KEY, 
    common_name VARCHAR(70) NOT NULL, 
    description VARCHAR(500) NOT NULL,
    cares VARCHAR(500) NOT NULL, 
    photo_link VARCHAR(120) NOT NULL,  
);