from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    #favorites = relationship('Product', secondary=user_favorites, back_populates='favorited_by')
    addresses = db.relationship('Address', back_populates='user')
    orders = db.relationship('Order', back_populates='user') 
    cart = db.relationship('Cart', back_populates='user') 

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)  # El precio de cada producto
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Relaciones con otras tablas
    category = db.relationship('Category', back_populates='products')
    
    def __repr__(self):
        return f'<Product {self.name}>'

    def serialize(self):
        # Incluye el campo price en el diccionario serializado
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,  # Agrega el precio aquí
            "category_id": self.category_id,
        }

    
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relación con User
    user = db.relationship("User", back_populates='cart')
    
    # Relación con CartItems
    items = db.relationship("CartItems", back_populates='cart')  # Bidireccional con CartItems

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

class CartItems(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    # Relación con Cart
    cart = db.relationship("Cart", back_populates='items')  # Bidireccional con Cart
    
    # Relación con Product
    product = db.relationship("Product")

    
class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), nullable=False)  # ejemplo: 'pending', 'shipped', 'delivered'
    sub_amount = db.Column(db.String(50), nullable=False)
    tax = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.String(50), nullable=False)
    
    user = db.relationship('User', back_populates='orders')
    order_details = db.relationship('Order_details', back_populates='order')

    def __repr__(self):
        return f'<Order {self.id}>'


    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
        }
    
class Order_details(db.Model):
    __tablename__ = 'order_details'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    amount = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))


    
    
    #user = relationship('User', back_populates='orders')
    order = db.relationship('Order', back_populates='order_details')
    product = db.relationship('Product', backref = 'details')

    def __repr__(self):
        return f'<Order_details {self.id}>'


    def serialize(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "price": self.price,
            "quantity": self.quantity,
            "amount": self.amount,
            "status": self.status,
        }

class Return(db.Model):
    __tablename__ = 'return'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    order_id = db.Column(db.Integer,db.ForeignKey("order.id"),nullable=False)
    reason = db.Column(db.String(120),nullable=False)
    order = db.relationship('Order', backref='returns')

    def __repr__(self):
        return f'<Return {self.id}>'


    def serialize(self):
        return {
            "id": self.id,
            "order_id" : self.order_id,
            "reason" : self.reason
            
        }

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    products = db.relationship('Product', back_populates='category')

    def __repr__(self):
        return f'<Category {self.name}>'


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Pay(db.Model):
    __tablename__ = 'payment'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # ejemplo: 'paid', 'pending', 'failed'

    def __repr__(self):
        return f'<Pay {self.order_id}>'


    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "status": self.status,
        }

class Address(db.Model):
    __tablename__ = 'address'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    street = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='addresses')

    def __repr__(self):
        return f'<Address {self.street}>'


    def serialize(self):
        return {
            "id": self.id,
            "street": self.street,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
        }


    
    