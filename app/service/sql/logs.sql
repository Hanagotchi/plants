CREATE SCHEMA IF NOT EXISTS dev;

CREATE TABLE IF NOT EXISTS dev.logs (
    id SERIAL PRIMARY KEY, 
    title VARCHAR(200) NOT NULL, 
    post_date DATETIME NOT NULL,
    last_update_date DATETIME NOT NULL, 
    content VARCHAR(1000) NOT NULL,
    plant_id 
);

CREATE TABLE IF NOT EXISTS dev.logs_photos (
    id SERIAL PRIMARY KEY,
    photo_link VARCHAR(120) NOT NULL, 
    CONSTRAINT fk_log
        FOREIGN KEY id_log
            REFERENCES logs(id)
);