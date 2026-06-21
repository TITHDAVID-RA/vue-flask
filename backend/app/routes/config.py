"""Configuration routes for frontend.

Exposes non-sensitive configuration to the frontend.
Stripe publishable key is safe to expose to the client.
"""

from flask import Blueprint, jsonify, current_app

config_bp = Blueprint('config', __name__)


@config_bp.route('/stripe-key', methods=['GET'])
def get_stripe_key():
    """Return Stripe publishable key to frontend.

    This is the PUBLIC key, safe to share with the client.
    The SECRET key remains in Key Vault and is only used server-side.
    """
    publishable_key = current_app.config.get('STRIPE_PUBLISHABLE_KEY')

    if not publishable_key:
        return jsonify({'error': 'Stripe publishable key not configured'}), 500

    return jsonify({
        'publishable_key': publishable_key,
        'message': 'Key retrieved securely from Azure Key Vault'
    })
