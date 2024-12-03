from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

products = []
DUMMY_API_URL = "https://dummyjson.com/products"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    global products
    if not products:
        try:
            response = requests.get(DUMMY_API_URL)
            response.raise_for_status()
            products = response.json().get('products', [])
        except requests.RequestException:
            return jsonify({"error": "Unable to fetch products from the API"}), 503
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    global products
    product_data = request.get_json()
    if not all(key in product_data for key in ['title', 'price', 'category']):
        return jsonify({"error": "Product must include 'title', 'price', and 'category'"}), 400
    products.append(product_data)
    return jsonify(products), 201

if __name__ == "__main__":
    app.run(debug=True)
