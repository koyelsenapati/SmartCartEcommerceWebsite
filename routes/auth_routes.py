from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint(
    "auth",
    __name__
)


# ===============================
# Register
# ===============================

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]


        if password != confirm_password:

            flash("Password does not match ❌")

            return redirect(
                url_for("auth.register")
            )


        hashed_password = generate_password_hash(password)


        try:

            connection = get_connection()
            cursor = connection.cursor()


            query = """
                INSERT INTO users
                (fullname, email, password)
                VALUES (%s, %s, %s)
            """


            cursor.execute(
                query,
                (
                    fullname,
                    email,
                    hashed_password
                )
            )


            connection.commit()


            flash("Registration Successful ✅")


            return redirect(
                url_for("auth.login")
            )


        except Exception:

            flash("Email already exists ❌")


        finally:

            cursor.close()
            connection.close()


    return render_template(
        "register.html"
    )


# ===============================
# Login
# ===============================

@auth.route("/login", methods=["GET", "POST"])
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


        cursor.execute(
            query,
            (email,)
        )


        user = cursor.fetchone()


        cursor.close()
        connection.close()


        if user and check_password_hash(
            user[3],
            password
        ):

            session["user_id"] = user[0]
            session["fullname"] = user[1]

            # Check your users table structure
            session["is_admin"] = user[5]


            flash(
                "Login Successful ✅"
            )


            return redirect(
                url_for("product.home")
            )


        else:

            flash(
                "Invalid Email or Password ❌"
            )


    return render_template(
        "login.html"
    )


# ===============================
# Logout
# ===============================

@auth.route("/logout")
def logout():

    session.clear()


    flash(
        "Logged Out Successfully 👋"
    )


    return redirect(
        url_for("auth.login")
    )