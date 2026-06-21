"""Health check and diagnostics routes."""

from flask import Blueprint, jsonify, current_app
from config import kv_config

health_bp = Blueprint('health', __name__)


@health_bp.route('/', methods=['GET'])
def health_check():
    """Basic health check."""
    return jsonify({
        'status': 'healthy',
        'service': 'SecureShop API',
        'key_vault_connected': kv_config.vault_url is not None,
        'key_vault_url': kv_config.vault_url
    })


@health_bp.route('/keyvault-status', methods=['GET'])
def keyvault_status():
    """Check Azure Key Vault connectivity and secret availability."""
    secrets_status = {}
    required_secrets = [
        'stripe-secret-key',
        'stripe-publishable-key',
        'jwt-secret-key',
        'database-url'
    ]

    for secret in required_secrets:
        try:
            value = kv_config.get_secret(secret)
            secrets_status[secret] = {
                'available': value is not None,
                'length': len(value) if value else 0,
                'source': 'key_vault' if kv_config.vault_url else 'environment'
            }
        except Exception as e:
            secrets_status[secret] = {
                'available': False,
                'error': str(e)
            }

    return jsonify({
        'key_vault_url': kv_config.vault_url,
        'secrets_status': secrets_status,
        'all_secrets_available': all(s.get('available') for s in secrets_status.values())
    })
