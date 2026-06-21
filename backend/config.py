"""
Application Configuration with Azure Key Vault Integration

This module handles all configuration for the Flask application.
Secrets (Stripe API keys, JWT secrets, DB credentials) are retrieved
from Azure Key Vault at runtime using Managed Identity authentication.
No secrets are ever stored in code or configuration files.
"""

import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.certificates import CertificateClient
from azure.keyvault.keys import KeyClient


class AzureKeyVaultConfig:
    """
    Centralized Azure Key Vault configuration manager.
    Retrieves secrets, certificates, and keys securely at runtime.
    """

    def __init__(self):
        self.vault_url = os.environ.get('AZURE_KEY_VAULT_URL')
        self.vault_name = os.environ.get('AZURE_KEY_VAULT_NAME')

        if not self.vault_url and self.vault_name:
            self.vault_url = f"https://{self.vault_name}.vault.azure.net"

        # Initialize credential - automatically uses Managed Identity on Azure
        # Falls back to Azure CLI, Visual Studio Code, or environment variables locally
        self.credential = DefaultAzureCredential()

        # Initialize clients for secrets, certificates, and keys
        self.secret_client = None
        self.certificate_client = None
        self.key_client = None

        if self.vault_url:
            self.secret_client = SecretClient(
                vault_url=self.vault_url,
                credential=self.credential
            )
            self.certificate_client = CertificateClient(
                vault_url=self.vault_url,
                credential=self.credential
            )
            self.key_client = KeyClient(
                vault_url=self.vault_url,
                credential=self.credential
            )

    def get_secret(self, secret_name):
        """Retrieve a secret from Azure Key Vault."""
        if not self.secret_client:
            return os.environ.get(secret_name.upper().replace('-', '_'))
        try:
            secret = self.secret_client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            print(f"Warning: Could not retrieve secret '{secret_name}' from Key Vault: {e}")
            # Fallback to environment variable for local development
            return os.environ.get(secret_name.upper().replace('-', '_'))

    def get_certificate(self, certificate_name):
        """Retrieve a certificate from Azure Key Vault."""
        if not self.certificate_client:
            return None
        try:
            certificate = self.certificate_client.get_certificate(certificate_name)
            return certificate
        except Exception as e:
            print(f"Warning: Could not retrieve certificate '{certificate_name}' from Key Vault: {e}")
            return None

    def get_key(self, key_name):
        """Retrieve a key from Azure Key Vault."""
        if not self.key_client:
            return None
        try:
            key = self.key_client.get_key(key_name)
            return key
        except Exception as e:
            print(f"Warning: Could not retrieve key '{key_name}' from Key Vault: {e}")
            return None


# Initialize Key Vault config
kv_config = AzureKeyVaultConfig()


class Config:
    """Base configuration class."""

    # Flask settings
    SECRET_KEY = kv_config.get_secret('flask-secret-key') or os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

    # Database - retrieved from Key Vault
    SQLALCHEMY_DATABASE_URI = kv_config.get_secret('database-url') or os.environ.get(
        'DATABASE_URL', 
        'sqlite:///ecommerce.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT - secret retrieved from Key Vault
    JWT_SECRET_KEY = kv_config.get_secret('jwt-secret-key') or os.environ.get('JWT_SECRET_KEY', 'jwt-dev-secret')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

    # Stripe - API keys retrieved from Key Vault at runtime
    # These are NEVER stored in code or config files
    STRIPE_SECRET_KEY = kv_config.get_secret('stripe-secret-key') or os.environ.get('STRIPE_SECRET_KEY', '')
    STRIPE_PUBLISHABLE_KEY = kv_config.get_secret('stripe-publishable-key') or os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
    STRIPE_WEBHOOK_SECRET = kv_config.get_secret('stripe-webhook-secret') or os.environ.get('STRIPE_WEBHOOK_SECRET', '')

    # Azure Key Vault settings
    AZURE_KEY_VAULT_URL = kv_config.vault_url

    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:8080,http://localhost:3000').split(',')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

    # In production, enforce that all secrets come from Key Vault
    @classmethod
    def validate(cls):
        """Validate that required secrets are available from Key Vault."""
        required_secrets = [
            'stripe-secret-key',
            'jwt-secret-key',
            'database-url'
        ]
        missing = []
        for secret in required_secrets:
            value = kv_config.get_secret(secret)
            if not value:
                missing.append(secret)
        if missing:
            raise RuntimeError(
                f"Missing required secrets in Azure Key Vault: {', '.join(missing)}. "
                f"Ensure Managed Identity has 'Key Vault Secrets User' role and secrets are created."
            )


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
