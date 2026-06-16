from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database.db import get_connection


product = Blueprint(
    "product",
    __name__
)


# ===============================
# Home Page - Best Seller Product
# ===============================

@product.route("/")
def home():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            products.id,
            products.name,
            products.description,
            products.price,
            products.image_url,
            SUM(order_items.quantity) AS total_sales

        FROM order_items

        JOIN products
        ON order_items.product_id = products.id

        GROUP BY products.id

        ORDER BY total_sales DESC

        LIMIT 1
    """

    cursor.execute(query)

    featured_product = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        featured_product=featured_product
    )


# ===============================
# All Products
# ===============================

@product.route("/products")
def products():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM products"
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "products.html",
        products=products
    )


# ===============================
# Single Product + Reviews
# ===============================

@product.route("/product/<int:id>")
def single_product(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    # Product Details
    query = """
        SELECT *
        FROM products
        WHERE id = %s
    """

    cursor.execute(query, (id,))

    item = cursor.fetchone()


    if not item:

        cursor.close()
        connection.close()

        flash("Product not found ❌")

        return redirect(
            url_for("product.products")
        )


    # Get Reviews
    review_query = """
        SELECT
            reviews.rating,
            reviews.comment,
            reviews.created_at,
            users.fullname

        FROM reviews

        JOIN users
        ON reviews.user_id = users.id

        WHERE reviews.product_id = %s

        ORDER BY reviews.created_at DESC
    """

    cursor.execute(
        review_query,
        (id,)
    )

    reviews = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "product.html",
        product=item,
        reviews=reviews
    )


# ===============================
# Search Product
# ===============================

@product.route("/search")
def search():

    keyword = request.args.get(
        "keyword",
        ""
    )

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    query = """
        SELECT *
        FROM products
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

@product.route("/category/<name>")
def category(name):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)


    query = """
        SELECT *
        FROM products
        WHERE category = %s
    """

    cursor.execute(
        query,
        (name,)
    )


    products = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "products.html",
        products=products
    )


# ===============================
# Add Product Review
# ===============================

@product.route("/review/<int:product_id>", methods=["POST"])
def add_review(product_id):

    if "user_id" not in session:

        flash("Please Login First ❌")

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    rating = request.form["rating"]

    comment = request.form["comment"]


    connection = get_connection()
    cursor = connection.cursor()


    query = """
        INSERT INTO reviews
        (user_id, product_id, rating, comment)
        VALUES (%s, %s, %s, %s)
    """


    cursor.execute(
        query,
        (
            user_id,
            product_id,
            rating,
            comment
        )
    )


    connection.commit()


    cursor.close()
    connection.close()


    flash("Review Added Successfully ⭐")


    return redirect(
        url_for(
            "product.single_product",
            id=product_id
        )
    )