SHOW DATABASES;

USE smartcart;

DESCRIBE users;
DESCRIBE products;
DESCRIBE cart;
DESCRIBE orders;
DESCRIBE order_items;

SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_items;
SELECT * FROM cart;
SELECT 
    product_id,
    SUM(quantity) AS total_sales

FROM order_items

GROUP BY product_id
ORDER BY total_sales DESC

LIMIT 1;

ALTER TABLE users
ADD is_admin BOOLEAN DEFAULT FALSE;

UPDATE users
SET is_admin = TRUE
WHERE email = "koyelsenapati5@gmail.com";

CREATE TABLE reviews (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    product_id INT NOT NULL,

    rating INT NOT NULL CHECK(rating BETWEEN 1 AND 5),

    comment TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);
SELECT * FROM reviews;