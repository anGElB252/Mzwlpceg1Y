# 代码生成时间: 2025-07-30 10:09:46
from quart import Quart, jsonify, request
from uuid import uuid4

# Initializing the app
app = Quart(__name__)

# In-memory store for cart data; in a real-world scenario,
# this would be replaced with a database.
cart_store = {}

# Helper function to create a unique cart ID
def create_cart_id():
    return str(uuid4())

# Helper function to find and return a cart from the cart store
def get_cart(cart_id):
    if cart_id not in cart_store:
        return None
    return cart_store[cart_id]

# Route to add an item to the cart
@app.route('/cart/add', methods=['POST'])
async def add_item_to_cart():
    try:
        data = await request.json
        cart_id = data.get('cart_id')
        item = data.get('item')
        quantity = data.get('quantity')

        if not cart_id or not item or not quantity or not isinstance(quantity, int):
            return jsonify({'error': 'Invalid data'}), 400

        cart = cart_store.get(cart_id)
        if not cart:
            cart = {}
            # Assign a new unique cart_id
            cart_id = create_cart_id()
            cart_store[cart_id] = cart

        # Add or update the item in the cart
        cart[item] = cart.get(item, 0) + quantity
        cart_store[cart_id] = cart

        return jsonify({'cart_id': cart_id, 'item': item, 'quantity': quantity}), 201
    except Exception as e:
        # Log the exception for debugging purposes
        return jsonify({'error': str(e)}), 500

# Route to get the cart contents
@app.route('/cart/<cart_id>', methods=['GET'])
async def get_cart_contents(cart_id):
    try:
        cart = get_cart(cart_id)
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404

        return jsonify(cart), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update the quantity of an item in the cart
@app.route('/cart/update', methods=['POST'])
async def update_item_quantity():
    try:
        data = await request.json
        cart_id = data.get('cart_id')
        item = data.get('item')
        quantity = data.get('quantity')

        if not cart_id or not item or not quantity or not isinstance(quantity, int):
            return jsonify({'error': 'Invalid data'}), 400

        cart = get_cart(cart_id)
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404

        # Update or remove the item in the cart
        if quantity > 0:
            cart[item] = quantity
        else:
            cart.pop(item, None)
            if not cart:
                # If the cart is empty, remove it from the store
                cart_store.pop(cart_id, None)

        return jsonify(cart), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start the Quart server
if __name__ == '__main__':
    app.run()
