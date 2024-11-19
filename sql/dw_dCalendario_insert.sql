-- Substitua as datas de início e término pelo período necessário
WITH RECURSIVE gerar_datas AS (
    SELECT DATE('2017-01-01') AS data
    UNION ALL
    SELECT DATE(data, '+1 day')
    FROM gerar_datas
    WHERE data < DATE('2018-08-31') -- Ajuste o período conforme necessário
)
INSERT INTO dw_dCalendario (data, ano, mes, dia, nome_mes, trimestre, semestre, semana_ano, dia_semana, nome_dia_semana, dia_util, ano_mes)
SELECT 
    data,
    CAST(STRFTIME('%Y', data) AS INTEGER) AS ano,
    CAST(STRFTIME('%m', data) AS INTEGER) AS mes,
    CAST(STRFTIME('%d', data) AS INTEGER) AS dia,
    CASE STRFTIME('%m', data)
        WHEN '01' THEN 'Janeiro'
        WHEN '02' THEN 'Fevereiro'
        WHEN '03' THEN 'Março'
        WHEN '04' THEN 'Abril'
        WHEN '05' THEN 'Maio'
        WHEN '06' THEN 'Junho'
        WHEN '07' THEN 'Julho'
        WHEN '08' THEN 'Agosto'
        WHEN '09' THEN 'Setembro'
        WHEN '10' THEN 'Outubro'
        WHEN '11' THEN 'Novembro'
        WHEN '12' THEN 'Dezembro'
    END AS nome_mes,
    CAST((CAST(STRFTIME('%m', data) AS INTEGER) - 1) / 3 + 1 AS INTEGER) AS trimestre,
    CAST((CAST(STRFTIME('%m', data) AS INTEGER) - 1) / 6 + 1 AS INTEGER) AS semestre,
    CAST(STRFTIME('%W', data) AS INTEGER) + 1 AS semana_ano,
    CAST(STRFTIME('%w', data) AS INTEGER) AS dia_semana,
    CASE STRFTIME('%w', data)
        WHEN '0' THEN 'Domingo'
        WHEN '1' THEN 'Segunda-feira'
        WHEN '2' THEN 'Terça-feira'
        WHEN '3' THEN 'Quarta-feira'
        WHEN '4' THEN 'Quinta-feira'
        WHEN '5' THEN 'Sexta-feira'
        WHEN '6' THEN 'Sábado'
    END AS nome_dia_semana,
    CASE WHEN STRFTIME('%w', data) IN ('0', '6') THEN 0 ELSE 1 END AS dia_util,
    STRFTIME('%Y-%m', data) AS ano_mes
FROM gerar_datas;
