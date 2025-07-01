import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS plans (
    id INTEGER PRIMARY KEY,
    plan_type TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    price REAL NOT NULL
);
''')

# Insert data
cursor.executemany('''
INSERT INTO plans (plan_type, ingredients, price)
VALUES (?, ?, ?);
''', [
    ('Standard', 'Chicken Wrap, Salad', 13000),
    ('Premium', 'Chicken/Beef Wrap, Salad, protein smoothie', 17000),
    ('Luxury', 'Chicken/Beef Wrap, Chowmein, fruit Salad, Fruit smoothie', 22000)
])

# Commit changes and close connection
conn.commit()
conn.close()
