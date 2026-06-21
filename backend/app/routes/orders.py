"""Order and payment processing routes.

Payment is processed using Stripe API keys retrieved from Azure Key Vault
at runtime via Managed Identity. No payment secrets are stored in code.
"""

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app import db

orders_bp = Blueprint('orders', __name__)


def get_stripe_client():
    """Initialize Stripe with secret key from Key Vault."""
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    return stripe


@orders_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order with Stripe payment processing.

    The Stripe secret key is retrieved from Azure Key Vault at runtime
    via Managed Identity authentication. It is never stored in code.
    """
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate items
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'No items in order'}), 400

    # Calculate total and validate products
    total = 0
    order_items = []

    for item_data in items:
        product = Product.query.get(item_data['id'])
        if not product:
            return jsonify({'error': f'Product {item_data["id"]} not found'}), 404

        quantity = item_data.get('quantity', 1)
        item_total = product.price * quantity
        total += item_total

        order_items.append({
            'product': product,
            'quantity': quantity,
            'price': product.price
        })

    # Process payment with Stripe
    # Stripe secret key retrieved from Azure Key Vault via Managed Identity
    stripe_client = get_stripe_client()

    try:
        # Create payment intent
        payment_intent = stripe_client.PaymentIntent.create(
            amount=int(total * 100),  # Convert to cents
            currency='usd',
            payment_method=data.get('payment_method_id'),
            confirmation_method='manual',
            confirm=True,
            metadata={
                'user_id': user_id,
                'order_items': str([{'id': i['product'].id, 'qty': i['quantity']} for i in order_items])
            }
        )

        # Create order
        order = Order(
            user_id=user_id,
            status='completed' if payment_intent.status == 'succeeded' else 'pending',
            total=total,
            stripe_payment_intent_id=payment_intent.id,
            shipping_address=data.get('shipping')
        )

        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create order items
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product'].id,
                quantity=item_data['quantity'],
                price_at_time=item_data['price']
            )
            db.session.add(order_item)

            # Update stock
            item_data['product'].stock -= item_data['quantity']

        db.session.commit()

        return jsonify({
            'success': True,
            'order': order.to_dict(),
            'payment_status': payment_intent.status
        })

    except stripe.error.CardError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': e.user_message or str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders for current user."""
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([o.to_dict() for o in orders])


@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get a specific order."""
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
    return jsonify(order.to_dict())
