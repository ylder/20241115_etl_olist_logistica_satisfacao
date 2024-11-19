WITH

filtered AS (
    SELECT * 
    FROM orders
    WHERE 
        -- Remover dados vazios, evitando influências ou dúvidas nos indicadores
        (
            order_id IS NOT NULL AND order_id != ''
            AND customer_id IS NOT NULL AND customer_id != ''
            AND order_status IS NOT NULL AND order_status != ''
            AND order_purchase_timestamp IS NOT NULL AND order_purchase_timestamp != ''
            AND order_approved_at IS NOT NULL AND order_approved_at != ''
            AND order_delivered_carrier_date IS NOT NULL AND order_delivered_carrier_date != ''
            AND order_delivered_customer_date IS NOT NULL AND order_delivered_customer_date != ''
            AND order_estimated_delivery_date IS NOT NULL AND order_estimated_delivery_date != ''
        )
        AND order_status = 'delivered'
        -- Período de baixa inconsistência nos dados
        AND order_approved_at BETWEEN '2017-01-01 00:00:00' AND '2018-08-31 23:59:59'
)

SELECT
    f.order_id,
    (c.customer_zip_code_prefix || c.customer_state) AS id_geolocation,
    DATE(f.order_approved_at) AS order_approved_at,
    
    -- Calculando a diferença em dias entre duas datas
    (
        CASE 
            WHEN (
                (
                    julianday(f.order_delivered_customer_date)
                    - julianday(DATETIME(f.order_estimated_delivery_date, '+23 hours', '+59 minutes', '+59 seconds'))
                ) * 24 / 24 > 0
            )
                THEN 'n'
            WHEN (
                (
                    julianday(f.order_delivered_customer_date)
                    - julianday(DATETIME(f.order_estimated_delivery_date, '+23 hours', '+59 minutes', '+59 seconds'))
                ) * 24 / 24 < 0
            )
                THEN 'y'
                ELSE 'y'
        END
    ) AS delivered_on_time,
    
    (julianday(f.order_delivered_customer_date) - julianday(f.order_delivered_carrier_date)) * 24 / 24 AS carrier_delivery_time,
    (julianday(f.order_delivered_carrier_date) - julianday(f.order_approved_at)) * 24 / 24 AS olist_delivery_time,
    (julianday(f.order_delivered_customer_date) - julianday(f.order_approved_at)) * 24 / 24 AS total_delivery_time
    
    FROM filtered AS f

    LEFT JOIN customers AS c
    ON c.customer_id = f.customer_id
    
    WHERE 
        carrier_delivery_time >= 0
        AND olist_delivery_time >= 0
        AND total_delivery_time >=0;