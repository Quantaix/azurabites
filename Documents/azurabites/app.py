from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'admins'

# Code for sqlite file connection for tables (zayem)

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

with open('sql.sql', 'r') as f:
    sql = f.read()
    cursor.executescript(sql)

conn.commit()
conn.close()

# end
# function for database connection (zayem)

def get_db_connection():
    con = sqlite3.connect('database.db')
    return con

#end

@app.route('/')
def my_func1():
    return render_template('index.html')

@app.route('/home', endpoint='home')
def my_func():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/ingredients')
def ingridients():
    return render_template('ingridients.html')

# registration route and form 'post' method (zayem)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']

        con = get_db_connection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM users WHERE user_name = ? AND password = ?',(user_name,password))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already taken','danger')
            redirect(url_for('register'))

        cursor.execute('INSERT INTO users (user_name,password)  VALUES (?,?)',(user_name,password))
        con.commit()
        con.close()
        # flash('Registration succesful')
        return redirect(url_for('login'))
    return render_template('register.html')

# login route and form (zayem)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        
        # Connect to database and check the user_name and password columns for infp (zayem)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_name = ? AND password = ?', (user_name, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0] 
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('login'))
    # return redirect(url_for('order'))
    return render_template('login.html')

@app.route('/orders')
def show_orders():
    if 'user_id' not in session:
        flash('You need to log in to view your orders.','danger')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn =  get_db_connection()
    cursor = conn.cursor()

    
    cursor.execute('''
        SELECT orders.id, users.user_name, orders.order_no, orders.purchase_date, orders.type
        FROM orders
        JOIN users ON orders.user_id = users.id
        WHERE orders.user_id = ?;
    ''', (user_id,)) 
    orders = cursor.fetchall()
    conn = conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/logout')
def logout():
    # session.clear()  # Clear all session data
    # flash('You have been logged out.', 'info')
    # return render_template('index.html')
    session.pop('user_id', None)
    return render_template('index.html')

@app.route('/membership')
def member():
    return render_template('membership.html')

@app.route('/checkout',methods=['GET', 'POST'])
def checkout():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        plan_id = request.form['plan_id']
        return redirect(url_for('payment', plan_id=plan_id))
    cursor.execute('SELECT * FROM plans')
    # plan = cursor.fetchone()
    plan = cursor.fetchall()
    conn.close()

    return render_template('checkout.html', plans=plan)

@app.route('/payment/<int:plan_id>', methods=['GET', 'POST'])
def payment(plan_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the selected plan details
    cursor.execute('SELECT * FROM plans WHERE id = ?', (plan_id,))
    plan = cursor.fetchone()
    conn.close()

    if request.method == 'POST':
        payment_method = request.form['payment_method']
        address = request.form['address']
        date_purchased = request.form['date_purchased']
        user_id = session.get('user_id')

        # Insert into checkout table
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO checkout (order_id, payment_method, address, date_purchased) VALUES (?, ?, ?, ?)',
                       (plan_id, payment_method, address, date_purchased))
        
        order_no = f"ORD-{int(plan_id)}-{int(user_id)}"  # Generate order number
        cursor.execute(
            'INSERT INTO orders (user_id, order_no, purchase_date, type) VALUES (?, ?, ?, ?)',
            (user_id, order_no, date_purchased, plan[1])  # Assuming plan[1] has the type or name
        )
        
        conn.commit()
        conn.close()

        return "Thank you! Your order has been processed." and redirect(url_for('home'))

    return render_template('payment.html', plan=plan)

if __name__== "__main__":
    app.run(debug=True)