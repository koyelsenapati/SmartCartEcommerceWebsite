from flask import Flask, render_template, request, flash, redirect, url_for, session
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "smartcart_secret_key"


# ===============================
# Home Page
# ===============================
@app.route("/")
def home():

    connection = get_connection()

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM products
        LIMIT 3
    """

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        products=products
    )


# ===============================
# Products Page (Dynamic)
# ===============================
@app.route("/products")
def products():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM products"

    cursor.execute(query)

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products
    )


# ===============================
# Single Product Page
# ===============================
@app.route("/product/<int:id>")
def product(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM products
        WHERE id = %s
    """

    cursor.execute(query, (id,))

    product = cursor.fetchone()

    cursor.close()
    connection.close()

    if not product:
        flash("Product not found ❌")
        return redirect(url_for("products"))

    return render_template(
        "product.html",
        product=product
    )


# ===============================
# Register Page
# ===============================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Password does not match ❌")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
                INSERT INTO users(fullname, email, password)
                VALUES(%s, %s, %s)
            """

            values = (
                fullname,
                email,
                hashed_password
            )

            cursor.execute(query, values)
            connection.commit()

            flash("Registration Successful ✅")
            return redirect(url_for("login"))

        except Exception:
            flash("Email already exists ❌")

        finally:
            cursor.close()
            connection.close()

    return render_template("register.html")


# ===============================
# Login Page
# ===============================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            SELECT * FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user and check_password_hash(user[3], password):

            session["user_id"] = user[0]
            session["fullname"] = user[1]

            flash("Login Successful ✅")

            return redirect(url_for("home"))

        else:
            flash("Invalid Email or Password ❌")

    return render_template("login.html")


# ===============================
# Logout
# ===============================
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully 👋")

    return redirect(url_for("login"))


# ===============================
# Cart Page (Protected)
# ===============================
@app.route("/cart")
def cart():

    if "user_id" not in session:

        flash("Please login first ❌")

        return redirect(url_for("login"))

    return render_template("cart.html")


# ===============================
# Add Product Page
# ===============================
@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        image_url = request.form["image_url"]
        stock = request.form["stock"]

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO products
            (name, description, price, image_url, stock)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            description,
            price,
            image_url,
            stock
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        flash("Product Added Successfully ✅")

        return redirect(url_for("add_product"))

    return render_template("add_product.html")


# ===============================
# Product Search
# ===============================
@app.route("/search")
def search():

    keyword = request.args.get("keyword", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM products
        WHERE name LIKE %s
    """

    cursor.execute(
        query,
        ("%" + keyword + "%",)
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products
    )


# ===============================
# Category Filter
# ===============================
@app.route("/category/<name>")
def category(name):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT * FROM products
        WHERE category = %s
    """

    cursor.execute(query, (name,))

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products
    )


# ===============================
# Run Flask Application
# ===============================
if __name__ == "__main__":
    app.run(debug=True)