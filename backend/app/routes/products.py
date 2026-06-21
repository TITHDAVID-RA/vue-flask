"""Product API routes."""

from flask import Blueprint, jsonify, request
from app.models.product import Product
from app import db

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products or filter by featured."""
    featured = request.args.get('featured', type=bool)

    query = Product.query
    if featured is not None:
        query = query.filter_by(featured=featured)

    products = query.all()
    return jsonify([p.to_dict() for p in products])


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@products_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product (admin only)."""
    data = request.get_json()

    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        image_url=data.get('image_url'),
        stock=data.get('stock', 0),
        featured=data.get('featured', False),
        category=data.get('category')
    )

    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@products_bp.route('/seed-products', methods=['POST'])
def seed_products():
    """Seed demo products into the database."""
    demo_products = [
        Product(
            name='Wireless Headphones Pro',
            description='Premium noise-cancelling wireless headphones with 30-hour battery life.',
            price=249.99,
            image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            stock=50,
            featured=True,
            category='Audio'
        ),
        Product(
            name='Smart Watch Ultra',
            description='Advanced fitness tracking with GPS, heart rate monitor, and 7-day battery.',
            price=399.99,
            image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            stock=30,
            featured=True,
            category='Wearables'
        ),
        Product(
            name='4K Webcam Studio',
            description='Professional 4K webcam with auto-focus and built-in ring light.',
            price=179.99,
            image_url='https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400',
            stock=100,
            featured=True,
            category='Accessories'
        ),
        Product(
            name='Mechanical Keyboard RGB',
            description='Hot-swappable mechanical keyboard with per-key RGB lighting.',
            price=149.99,
            image_url='https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400',
            stock=25,
            featured=False,
            category='Accessories'
        ),
        Product(
            name='Portable SSD 2TB',
            description='Ultra-fast NVMe portable SSD with USB-C connectivity.',
            price=199.99,
            image_url='https://images.unsplash.com/photo-1597872252165-4827a235d7bc?w=400',
            stock=40,
            featured=False,
            category='Storage'
        ),
        Product(
            name='USB-C Docking Station',
            description='12-in-1 USB-C docking station with dual 4K HDMI output.',
            price=129.99,
            image_url='https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400',
            stock=60,
            featured=False,
            category='Accessories'
        )
    ]

    for product in demo_products:
        existing = Product.query.filter_by(name=product.name).first()
        if not existing:
            db.session.add(product)

    db.session.commit()
    return jsonify({'message': 'Products seeded successfully'}), 201
