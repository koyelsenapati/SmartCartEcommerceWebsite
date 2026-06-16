from flask import Flask

from routes.auth_routes import auth
from routes.product_routes import product
from routes.cart_routes import cart
from routes.order_routes import order
from routes.admin_routes import admin


# ===============================
# Flask Application
# ===============================

app = Flask(__name__)


# Secret Key for Session
app.secret_key = "smartcart_secret_key"


# ===============================
# Register All Blueprints
# ===============================

app.register_blueprint(auth)
app.register_blueprint(product)
app.register_blueprint(cart)
app.register_blueprint(order)
app.register_blueprint(admin)


# ===============================
# Run Flask Application
# ===============================

if __name__ == "__main__":

    app.run(
        debug=True
    )