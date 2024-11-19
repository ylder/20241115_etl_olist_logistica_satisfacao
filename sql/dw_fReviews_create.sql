CREATE TABLE IF NOT EXISTS dw_fReviews (
    review_id TEXT,
    order_id TEXT,
    nps_rated_review TEXT,
    PRIMARY KEY (review_id, order_id),
    FOREIGN KEY(order_id) REFERENCES dw_fOrders(order_id)
)