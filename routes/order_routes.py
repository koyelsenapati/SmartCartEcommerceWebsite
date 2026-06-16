from flask import Blueprint, render_template, session, redirect, url_for, flash
from database.db import get_connection


order = Blueprint(
    "order",
    __name__
)


# ===============================
# Checkout System
# ===============================

@order.route("/checkout")
def checkout():

    if "user_id" not in session:

        flash("Please login first ❌")

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor(dictionary=True)


    # Get cart products
    query = """
        SELECT 
            products.id,
            products.price,
            cart.quantity

        FROM cart

        JOIN products
        ON cart.product_id = products.id

        WHERE cart.user_id = %s
    """


    cursor.execute(
        query,
        (user_id,)
    )


    items = cursor.fetchall()


    # Check empty cart
    if not items:

        cursor.close()
        connection.close()

        flash("Cart is empty ❌")

        return redirect(
            url_for("cart.view_cart")
        )


    # Calculate total price
    total_price = 0

    for item in items:

        total_price += item["price"] * item["quantity"]


    # Create order
    query = """
        INSERT INTO orders
        (user_id, total_price)

        VALUES (%s, %s)
    """


    cursor.execute(
        query,
        (
            user_id,
            total_price
        )
    )


    order_id = cursor.lastrowid


    # Insert order items
    for item in items:


        query = """
            INSERT INTO order_items
            (order_id, product_id, quantity, price)

            VALUES (%s, %s, %s, %s)
        """


        cursor.execute(
            query,
            (
                order_id,
                item["id"],
                item["quantity"],
                item["price"]
            )
        )


    # Clear user cart
    query = """
        DELETE FROM cart
        WHERE user_id = %s
    """


    cursor.execute(
        query,
        (user_id,)
    )


    connection.commit()


    cursor.close()
    connection.close()


    flash(
        "Order placed successfully 🎉"
    )


    return redirect(
        url_for("product.home")
    )


# ===============================
# My Orders History
# ===============================

@order.route("/orders")
def my_orders():

    if "user_id" not in session:

        flash(
            "Please login first ❌"
        )

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]


    connection = get_connection()

    cursor = connection.cursor(dictionary=True)


    query = """
        SELECT
            id,
            total_price,
            order_date

        FROM orders

        WHERE user_id = %s

        ORDER BY order_date DESC
    """


    cursor.execute(
        query,
        (user_id,)
    )


    orders = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "orders.html",
        orders=orders
    )