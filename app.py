from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db', 'products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializar o banco de dados
db = SQLAlchemy(app)

# Definir o modelo do Produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __init__(self, name, quantity, value, category):
        self.name = name
        self.quantity = quantity
        self.value = value
        self.category = category

# Rotas da API
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = [{
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'value': product.value,
        'category': product.category
    } for product in products]
    return jsonify(result)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):

    product = Product.query.get_or_404(product_id)
    result = {
        'id': product.id,
        'name': product.name,
        'quantity': product.quantity,
        'value': product.value,
        'category': product.category
    }
    return jsonify(result)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(name=data['name'], quantity=data['quantity'], value=data['value'], category=data['category'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully!'}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json
    product.name = data['name']
    product.quantity = data['quantity']
    product.value = data['value']
    product.category = data['category']
    db.session.commit()
    return jsonify({'message': 'Product updated successfully!'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully!'})

if __name__ == '__main__':
    # Criar o banco de dados se não existir
    with app.app_context():
        db.create_all()
    app.run(debug=True)