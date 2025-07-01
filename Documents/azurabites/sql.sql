CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY ,
    user_name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY ,
    user_id INTEGER NOT NULL,
    order_no TEXT NOT NULL,
    purchase_date TEXT NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);


SELECT orders.id, users.user_name, orders.order_no, orders.purchase_date, orders.type
FROM orders
JOIN users ON orders.user_id = users.id
WHERE orders.user_id = ?;

CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY,
    plan_type TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    price REAL NOT NULL
);

-- INSERT INTO plans ( plan_type, ingredients, price)
-- VALUES ('Standard', 'Chicken Wrap,Salad', 13000);
--   ('Premium', 'Chicken/Beef Wrap,Salad,protein smoothie', 17000),
--   ('Luxury', 'Chicken/Beef Wrap,Chowmein,fruit Salad,Fruit smoothie', 22000);

CREATE TABLE IF NOT EXISTS checkout (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_method TEXT NOT NULL,
    address TEXT NOT NULL,
    date_purchased TEXT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES plans (id)
);