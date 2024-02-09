CREATE SCHEMA IF NOT EXISTS dev;

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE 
    IF NOT EXISTS dev.plants (
        id SERIAL PRIMARY KEY, 
        user_id SERIAL NOT NULL,
        name VARCHAR(64) NOT NULL, 
        scientific_name VARCHAR(64) NOT NULL
);
DO $do$ BEGIN
    IF (SELECT COUNT(*) FROM dev.plants) = 0 THEN
        INSERT INTO dev.plants (user_id, name, scientific_name) VALUES 
            (1, 'Rosa', 'Rosa'),
            (2, 'Margarita', 'Margarita'),
            (3, 'Girasol', 'Girasol');
    END IF;
END $do$;

CREATE TABLE IF NOT EXISTS dev.logs (
    id SERIAL PRIMARY KEY, 
    title VARCHAR(200) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    content VARCHAR(1000) NOT NULL,
    plant_id INT,
    CONSTRAINT fk_plant
        FOREIGN KEY (plant_id)
            REFERENCES dev.plants(id)
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON dev.logs
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

CREATE TABLE IF NOT EXISTS dev.logs_photos (
    id SERIAL PRIMARY KEY,
    log_id INT,
    photo_link VARCHAR(120) NOT NULL, 
    CONSTRAINT fk_log
        FOREIGN KEY (log_id)
            REFERENCES dev.logs(id)
);