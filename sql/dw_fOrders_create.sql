CREATE TABLE IF NOT EXISTS dw_fOrders (
    order_id TEXT PRIMARY KEY,
    id_geolocation TEXT,
    order_approved_at DATE,
    delivered_on_time TEXT,
    carrier_delivery_time REAL,
    olist_delivery_time REAL,
    total_delivery_time REAL,
    FOREIGN KEY(order_approved_at) REFERENCES dw_dCalendario(data),
    FOREIGN KEY(id_geolocation) REFERENCES dw_dGeolocation(id_geolocation)
)