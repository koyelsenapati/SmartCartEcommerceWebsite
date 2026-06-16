from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db import get_connection


cart = Blueprint(
    "cart",
    __name__
)


# ===============================
# View Cart
# ===============================

@cart.route("/cart")
def view_cart():

    if "user_id" not in session:
        flash("Please login first ❌")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT 
            cart.id,
            products.name,
            products.price,
            products.image_url,
            cart.quantity,
            (products.price * cart.quantity) AS total
        FROM cart
        JOIN products
        ON cart.product_id = products.id
        WHERE cart.user_id = %s
    """

    cursor.execute(query, (user_id,))
    cart_items = cursor.fetchall()

    grand_total = 0

    for item in cart_items:
        grand_total += item["total"]

    cursor.close()
    connection.close()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        grand_total=grand_total
    )


# ===============================
# Add To Cart
# ===============================

@cart.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    if "user_id" not in session:
        flash("Please login first ❌")
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM cart
        WHERE user_id=%s AND product_id=%s
    """

    cursor.execute(query, (user_id, id))

    item = cursor.fetchone()

    if item:

        query = """
            UPDATE cart
            SET quantity = quantity + 1
            WHERE id=%s
        """

        cursor.execute(query, (item["id"],))

    else:

        query = """
            INSERT INTO cart
            (user_id, product_id, quantity)
            VALUES(%s, %s, 1)
        """

        cursor.execute(query, (user_id, id))


    connection.commit()

    cursor.close()
    connection.close()

    flash("Product added to cart 🛒")

    return redirect(url_for("cart.view_cart"))


# ===============================
# Increase Quantity
# ===============================

@cart.route("/increase/<int:id>")
def increase(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE cart
        SET quantity = quantity + 1
        WHERE id=%s
    """

    cursor.execute(query, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("cart.view_cart"))


# ===============================
# Decrease Quantity
# ===============================

@cart.route("/decrease/<int:id>")
def decrease(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT quantity
        FROM cart
        WHERE id=%s
    """

    cursor.execute(query, (id,))

    item = cursor.fetchone()

    if not item:

        cursor.close()
        connection.close()

        flash("Item not found ❌")

        return redirect(url_for("cart.view_cart"))


    quantity = item[0]


    if quantity > 1:

        query = """
            UPDATE cart
            SET quantity = quantity - 1
            WHERE id=%s
        """

    else:

        query = """
            DELETE FROM cart
            WHERE id=%s
        """


    cursor.execute(query, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("cart.view_cart"))


# ===============================
# Remove Item
# ===============================

@cart.route("/remove/<int:id>")
def remove(id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM cart
        WHERE id=%s
    """

    cursor.execute(query, (id,))

    connection.commit()

    cursor.close()
    connection.close()

    flash("Item removed 🗑️")

    return redirect(url_for("cart.view_cart"))