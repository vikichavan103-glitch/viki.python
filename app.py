from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "ecommerce_secret_key"

# Product data
products = [
    {
        "id": 1,
        "name": "Smartphone",
        "price": 15999,
        "image": "https://via.placeholder.com/250?text=Smartphone"
    },
    {
        "id": 2,
        "name": "Laptop",
        "price": 54999,
        "image": "https://via.placeholder.com/250?text=Laptop"
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 1999,
        "image": "https://via.placeholder.com/250?text=Headphones"
    },
    {
        "id": 4,
        "name": "Smart Watch",
        "price": 2999,
        "image": "https://via.placeholder.com/250?text=Smart+Watch"
    }
]


@app.route("/")
def index():
    return render_template("index.html", products=products)


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])

    if product_id not in cart:
        cart.append(product_id)

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/remove_from_cart/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])
    cart_products = []

    for product in products:
        if product["id"] in cart_ids:
            cart_products.append(product)

    total = sum(product["price"] for product in cart_products)

    return render_template(
        "cart.html",
        cart_products=cart_products,
        total=total
    )


@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]

        # Clear cart after order
        session["cart"] = []

        return f"""
        <h1>Order Placed Successfully!</h1>
        <p>Thank you, {name}.</p>
        <p>Your order will be delivered to:</p>
        <p>{address}</p>
        <a href="/">Continue Shopping</a>
        """

    return render_template("checkout.html")


if __name__ == "__main__":
    app.run(debug=True)