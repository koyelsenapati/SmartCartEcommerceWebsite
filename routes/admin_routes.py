from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from database.db import get_connection


admin = Blueprint(
    "admin",
    __name__
)


# ===============================
# Admin Dashboard
# ===============================

@admin.route("/dashboard")
def dashboard():

    if not session.get("is_admin"):

        flash("Admin Access Only ❌")

        return redirect(
            url_for("product.home")
        )


    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    cursor.execute("""
        SELECT COUNT(*) AS total_users
        FROM users
    """)
    users = cursor.fetchone()


    cursor.execute("""
        SELECT COUNT(*) AS total_products
        FROM products
    """)
    products = cursor.fetchone()


    cursor.execute("""
        SELECT COUNT(*) AS total_orders
        FROM orders
    """)
    orders = cursor.fetchone()


    cursor.execute("""
        SELECT SUM(total_price) AS revenue
        FROM orders
    """)
    revenue = cursor.fetchone()


    cursor.close()
    connection.close()


    return render_template(
        "admin_dashboard.html",
        users=users,
        products=products,
        orders=orders,
        revenue=revenue
    )


# ===============================
# Admin Product List
# ===============================

@admin.route("/products")
def products():

    if not session.get("is_admin"):

        flash("Admin Access Only ❌")

        return redirect(
            url_for("product.home")
        )


    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    cursor.execute("""
        SELECT *
        FROM products
    """)

    products = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "admin_products.html",
        products=products
    )


# ===============================
# Add Product
# ===============================

@admin.route("/add-product", methods=["GET", "POST"])
def add_product():

    if not session.get("is_admin"):

        flash("Admin Access Only ❌")

        return redirect(
            url_for("product.home")
        )


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


        cursor.execute(
            query,
            (
                name,
                description,
                price,
                image_url,
                stock
            )
        )


        connection.commit()


        cursor.close()
        connection.close()


        flash("Product Added Successfully ✅")


        return redirect(
            url_for("admin.products")
        )


    return render_template(
        "add_product.html"
    )


# ===============================
# Edit Product
# ===============================

@admin.route("/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if not session.get("is_admin"):

        flash("Admin Access Only ❌")

        return redirect(
            url_for("product.home")
        )


    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    if request.method == "POST":

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        image_url = request.form["image_url"]
        stock = request.form["stock"]


        query = """
            UPDATE products
            SET
                name=%s,
                description=%s,
                price=%s,
                image_url=%s,
                stock=%s
            WHERE id=%s
        """


        cursor.execute(
            query,
            (
                name,
                description,
                price,
                image_url,
                stock,
                id
            )
        )


        connection.commit()


        cursor.close()
        connection.close()


        flash(
            "Product Updated Successfully ✅"
        )


        return redirect(
            url_for("admin.products")
        )


    query = """
        SELECT *
        FROM products
        WHERE id=%s
    """


    cursor.execute(
        query,
        (id,)
    )


    product = cursor.fetchone()


    if not product:

        cursor.close()
        connection.close()


        flash(
            "Product not found ❌"
        )


        return redirect(
            url_for("admin.products")
        )


    cursor.close()
    connection.close()


    return render_template(
        "edit_product.html",
        product=product
    )


# ===============================
# Delete Product
# ===============================

@admin.route("/delete-product/<int:id>")
def delete_product(id):

    if not session.get("is_admin"):

        flash("Admin Access Only ❌")

        return redirect(
            url_for("product.home")
        )


    connection = get_connection()
    cursor = connection.cursor()


    query = """
        DELETE FROM products
        WHERE id=%s
    """


    cursor.execute(
        query,
        (id,)
    )


    connection.commit()


    cursor.close()
    connection.close()


    flash(
        "Product Deleted Successfully 🗑️"
    )


    return redirect(
        url_for("admin.products")
    )