-- Esquema EPS — PostgreSQL
-- Usuarios: contraseña almacenada como hash (bcrypt) vía aplicación

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS medicamentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    es_pos BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_nombre_no_vacio CHECK (char_length(trim(nombre)) > 0)
);

CREATE TABLE IF NOT EXISTS solicitudes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    medicamento_id INTEGER NOT NULL REFERENCES medicamentos(id) ON DELETE RESTRICT,
    numero_orden VARCHAR(100),
    direccion VARCHAR(500),
    telefono VARCHAR(50),
    correo VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_solicitudes_usuario ON solicitudes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_created ON solicitudes(created_at DESC);

-- Datos iniciales de ejemplo
INSERT INTO medicamentos (nombre, es_pos)
SELECT * FROM (VALUES
    ('Acetaminofén 500 mg', TRUE::boolean),
    ('Ibuprofeno 400 mg', TRUE::boolean),
    ('Medicamento especial NO POS A', FALSE::boolean),
    ('Medicamento especial NO POS B', FALSE::boolean)
) AS t(nombre, es_pos)
WHERE NOT EXISTS (SELECT 1 FROM medicamentos LIMIT 1);
