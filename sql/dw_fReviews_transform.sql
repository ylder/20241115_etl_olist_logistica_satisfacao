WITH

    orders_transform AS (
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
                order_id,
                DATE(order_approved_at) AS order_approved_at,

                -- Calculando a diferença em dias entre duas datas
                (
                    CASE 
                        WHEN (
                            (
                                julianday(order_delivered_customer_date)
                                - julianday(DATETIME(order_estimated_delivery_date, '+23 hours', '+59 minutes', '+59 seconds'))
                            ) * 24 / 24 > 0
                        )
                            THEN 'n'
                        WHEN (
                            (
                                julianday(order_delivered_customer_date)
                                - julianday(DATETIME(order_estimated_delivery_date, '+23 hours', '+59 minutes', '+59 seconds'))
                            ) * 24 / 24 < 0
                        )
                            THEN 'y'
                            ELSE 'y'
                    END
                ) AS delivered_on_time,
                
                (julianday(order_delivered_customer_date) - julianday(order_delivered_carrier_date)) * 24 / 24 AS carrier_delivery_time,
                (julianday(order_delivered_carrier_date) - julianday(order_approved_at)) * 24 / 24 AS olist_delivery_time,
                (julianday(order_delivered_customer_date) - julianday(order_approved_at)) * 24 / 24 AS total_delivery_time
                
                FROM filtered
                
                WHERE 
                    carrier_delivery_time >= 0
                    AND olist_delivery_time >= 0
                    AND total_delivery_time >=0
    ),

    filtered AS (

        SELECT
            r.review_id,
            r.order_id,
            r.review_score

        FROM reviews AS r

        INNER JOIN orders_transform AS o
            ON o.order_id = r.order_id
    )

    SELECT
        review_id,
        order_id,
        (
            CASE
                WHEN review_score <= 3 THEN 'detrator'
                WHEN review_score = 4 THEN 'neutral'
                ELSE 'promoter'
            END
        ) AS nps_rated_review

    FROM filtered;
