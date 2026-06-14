from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "smartcart_secret_key"


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Products Page
@app.route("/products")
def products():
    return render_template("products.html")


# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password == confirm_password:
            flash("Registration Successful ✅")
        else:
            flash("Password does not match ❌")

    return render_template("register.html")


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        print("Email:", email)
        print("Password:", password)

    return render_template("login.html")


# Cart Page
@app.route("/cart")
def cart():
    return render_template("cart.html")


# Dynamic Product Page
@app.route("/product/<int:id>")
def product(id):
    return render_template(
        "product.html",
        product_id=id
    )


if __name__ == "__main__":
    app.run(debug=True)