import os

from cs50 import SQL

from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# configure app
app = Flask(__name__)

# Global dictionary


# configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")





@app.route("/")
def index():
    name= session.get("name")

    products = db.execute("SELECT * FROM products ORDER BY product_name")



    return render_template("index.html", name=name, products=products)






@app.route("/adminLogin", methods=["GET", "POST"])
def adminLogin():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = db.execute("SELECT * FROM admins WHERE username = ?", username)

        if len(admin) != 1:
            return "invalid username"
        if admin[0]["password"] != password:
            return "invalid password"
        session["admin_id"] = admin[0]["id"]

        return redirect ("/adminDashboard")
    return render_template("adminLogin.html")


@app.route("/adminDashboard")
def adminDashboard():

    # Check if the admin is logged in
    if "admin_id" not in session:
        return redirect("/adminLogin")
    return render_template("adminDashboard.html")


@app.route("/adminProducts", methods=["GET", "POST"])
def adminProducts():

    # Prevent unauthorized access
    if "admin_id" not in session:
        return redirect("/adminLogin")

    # If the admin submits the form
    if request.method == "POST":

        product_name = request.form.get("product_name")
        price = request.form.get("price")

        existing = db.execute("SELECT id FROM products WHERE product_name = ?", product_name)

        if existing:
            return "Product already exist."

        # Save the product
        db.execute("INSERT INTO products(product_name, price) VALUES(?, ?)", product_name, price)

        return redirect("/adminProducts")





    # Retrieve all products
    products = db.execute("SELECT * FROM products ORDER BY product_name")

    return render_template("adminProducts.html", products=products)



# search route
@app.route("/searchProducts", methods=["GET", "POST"])
def searchRoute():
    search = request.args.get("search", "").strip()

    if search:
        products = db.execute("SELECT * FROM products WHERE product_name LIKE ? ORDER BY product_name", "%" + search + "%")

    else:
        products = db.execute("SELECT * FROM products ORDER BY product_name")

    return render_template("adminProducts.html", products=products, search=search)



@app.route("/adminEditProduct/<int:product_id>", methods=["GET", "POST"])
def adminEditProduct(product_id):
    if "admin_id" not in session:
        return redirect("/adminLogin")

    if request.method == "POST":
        product_name = request.form.get("product_name")
        price = request.form.get("price")

        db.execute("UPDATE products SET product_name = ?, price = ? WHERE id =?", product_name, price, product_id)

        return redirect("/adminProducts")

    product = db.execute(
        "SELECT * FROM products WHERE id = ?",
        product_id
    )

    return render_template("adminEditProduct.html", product=product[0])


@app.route("/adminDeleteProduct/<int:product_id>")
def adminDeleteProduct(product_id):

    if "admin_id" not in session:
        return redirect("/adminLogin")

    db.execute("DELETE FROM products WHERE id = ?", product_id)

    return redirect("/adminProducts")



@app.route("/viewOrders")
def viewOrders():

    # prevent unauthorized access
    if "admin_id" not in session:
        return redirect("/adminLogin")


    # get every order with the customers name
    orders = db.execute("""
    SELECT
        orders.id,
        customers.name,
        orders.total,
        orders.order_date
    FROM orders
    JOIN customers
        ON orders.customer_id = customers.id
    ORDER BY orders.order_date DESC
    """)

    return render_template("viewOrders.html", orders=orders)


@app.route("/orderDetails/<int:order_id>")
def orderDetails(order_id):

    # Prevent unauthorized access
    if "admin_id" not in session:
        return redirect("/adminLogin")

    # Get order information
    order = db.execute("""
        SELECT
            orders.id,
            customers.name,
            orders.total,
            orders.order_date
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.id
        WHERE orders.id = ?
    """, order_id)

    if len(order) == 0:
        return "Order not found."

    # Get all products in this order

    items = db.execute("""
        SELECT
            product_name,
            unit_price,
            quantity,
            subtotal
        FROM order_items
         WHERE order_id = ?
    """, order_id)

    return render_template("orderDetails.html", order=order[0], items=items)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name").strip()

        if not name:
            return"please enter your name"

        session["name"] = name

        return redirect("/")

    return render_template("login.html")



# user search route
@app.route("/userSearch", methods=["GET", "POST"])
def userSearch():
    search = request.args.get("search", "").strip()

    if search:
        products = db.execute("SELECT * FROM products WHERE product_name LIKE ? ORDER BY product_name", "%" + search + "%")

    else:
        products = db.execute("SELECT * FROM products ORDER BY product_name")

    return render_template("order.html", products=products, search=search)





@app.route("/order")
def order():
    name= session.get("name")

    products = db.execute("SELECT * FROM products ORDER BY product_name")
    return render_template("order.html", name=name, products=products)


@app.route("/submit_order", methods=["POST"])
def submit_order():

    # Get customers name
    name = session.get("name")

    if not name:
        return redirect("/login")

    # Get or create customer
    customer = db.execute("SELECT * FROM customers WHERE name = ?", name)

    if len(customer) == 0:

        db.execute("INSERT INTO customers(name) VALUES(?)", name)

        # Read customer again after inserting

        customer = db.execute("SELECT * FROM customers WHERE name = ?", name)

    customer_id = customer[0]["id"]

    # read products from database

    products = db.execute("SELECT * FROM products ORDER BY product_name")

    order = []

    grand_total = 0

    # Read customers selections

    for product in products:
        quantity = float(request.form.get(product["product_name"], 0) or 0)

        if quantity <= 0:

            continue

        subtotal = quantity * product["price"]

        grand_total += subtotal

        order.append({
            "product": product["product_name"],
            "price": product["price"],
            "quantity": quantity,
            "total": subtotal
        })

    # No products selected

    if len(order) == 0:
        return "please select at least one product."

    #save order

    db.execute("INSERT INTO orders(customer_id, total) VALUES(?, ?)", customer_id, grand_total)

    # Get ID of newly inserted order

    order_id = db.execute("SELECT last_insert_rowid() AS id")[0]["id"]

    # Save each ordered item

    for item in order:
        db.execute("INSERT INTO order_items(order_id, product_name, unit_price, quantity, subtotal) VALUES(?, ?, ?, ?, ?)", order_id, item["product"], item["price"], item["quantity"], item["total"])


    return render_template("yourOrder.html", name=name, order=order, grand_total=grand_total)




@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

