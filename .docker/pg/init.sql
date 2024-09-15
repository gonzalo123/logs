-- Crear la tabla de logs
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP NOT NULL,
    log_level VARCHAR(10) NOT NULL,
    log_text TEXT NOT NULL,
    extra_data JSONB,
    hash CHAR(32) NOT NULL
);

-- Crear un índice en la columna "time" para búsquedas por rango de tiempo
CREATE INDEX idx_logs_time ON logs (time);

-- Crear un índice en la columna "log_level" para filtrar por nivel de log
CREATE INDEX idx_logs_level ON logs (log_level);

-- Crear un índice GIN en la columna "extra_data" para realizar búsquedas eficientes dentro del campo JSON
CREATE INDEX idx_logs_extra_data ON logs USING GIN (extra_data);

-- Crear un índice en la columna "hash" para búsquedas rápidas por hash
CREATE INDEX idx_logs_hash ON logs (hash);

ALTER TABLE logs ADD CONSTRAINT unique_hash UNIQUE (hash);
