CREATE TABLE IF NOT EXISTS dw_dCalendario (
    data DATE PRIMARY KEY,
    ano INTEGER,
    mes INTEGER,
    dia INTEGER,
    nome_mes TEXT,
    trimestre INTEGER,
    semestre INTEGER,
    semana_ano INTEGER,
    dia_semana INTEGER,
    nome_dia_semana TEXT,
    dia_util INTEGER,
    ano_mes TEXT
)