CREATE SCHEMA IF NOT EXISTS dev;

CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS dev.logs (
    id SERIAL PRIMARY KEY, 
    title VARCHAR(200) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    content VARCHAR(1000) NOT NULL
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