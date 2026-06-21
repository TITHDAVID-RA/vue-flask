#!/usr/bin/env python3
"""
SecureShop Flask Application Entry Point

This application demonstrates secure SaaS architecture using:
- Azure App Service for hosting
- Azure Key Vault for secret management
- Azure Managed Identity for passwordless authentication
- Stripe for payment processing with secrets from Key Vault

Security Flow (as shown in the UI):
1. User accesses the SaaS application
2. Application is hosted on Azure App Service
3. App Service uses Managed Identity to authenticate to Azure Key Vault
4. Key Vault returns the payment API secret securely
5. Secret is used at runtime, never stored in code or configuration
"""

import os
from app import create_app, db
from app.models.user import User
from app.models.product import Product

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.cli.command('seed')
def seed_db():
    """Seed the database with demo data."""
    with app.app_context():
        # Create demo user
        if not User.query.filter_by(email='demo@secureshop.com').first():
            user = User(email='demo@secureshop.com', name='Demo User')
            user.set_password('demo123')
            db.session.add(user)

        # Seed products via API endpoint
        from app.routes.products import seed_products
        with app.test_client() as client:
            client.post('/api/seed-products')

        db.session.commit()
        print('Database seeded successfully!')


@app.cli.command('create-admin')
def create_admin():
    """Create an admin user."""
    import click
    email = click.prompt('Email')
    name = click.prompt('Name')
    password = click.prompt('Password', hide_input=True)

    with app.app_context():
        user = User(email=email, name=name, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f'Admin user {email} created successfully!')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
