from application.database import db
from sqlalchemy.orm import relationship
from flask_security import UserMixin, RoleMixin




# Models for the app
class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    password = db.Column(db.String, nullable = False)
    dob = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean(), nullable = False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String, db.ForeignKey("role.name"))



class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True)
    description = db.Column(db.String(255))



class Products(db.Model):
    __tablename__='product'
    product_id = db.Column(db.Integer, nullable = False, autoincrement = True, unique = True, primary_key = True)
    product_name = db.Column(db.String, nullable = False,unique = True)
    unit = db.Column(db.String, nullable = False)
    rate = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Float, nullable = False)
    category = db.Column(db.String, db.ForeignKey("category.category_name",onupdate="CASCADE"), nullable = False )
    sold = db.Column(db.Float, nullable = False)


class Category(db.Model):
    __tablename__='category'
    category_id = db.Column(db.Integer, nullable = False, autoincrement = True, unique = True, primary_key = True)
    category_name = db.Column(db.String, nullable = False,unique = True)
    product = relationship("Products", cascade = "all,delete", backref = "product")


class Sale(db.Model):
    __tablename__='order'
    sale_id =  db.Column(db.Integer, nullable = False, autoincrement = True, unique = True, primary_key = True)
    username = db.Column(db.String, nullable = False)
    product = db.Column(db.String, nullable = False)
    quantity = db.Column(db.Float, nullable = False)
    rate = db.Column(db.Float, nullable = False)
    cost = db.Column(db.Float, nullable = False)


class Orders(db.Model):
    __tablename__='sale'
    order_id =  db.Column(db.Integer, nullable = False, autoincrement = True, unique = True, primary_key = True)
    username = db.Column(db.String, nullable = False)
    total_sale = db.Column(db.Float, nullable = False)
    address = db.Column(db.String, nullable = False)
    mode_of_payment = db.Column(db.String, nullable = False)
    date = db.Column(db.String, nullable = False)



class Requests(db.Model) : 
    __tablename__='Requests'
    request_id = db.Column(db.Integer, nullable = False, autoincrement = True, unique = True, primary_key = True)
    type = db.Column(db.String, nullable = False)
    old_name = db.Column(db.String, db.ForeignKey("category.category_name"))
    by = db.Column(db.String, nullable = False)
    date = db.Column(db.String, nullable = False)
    new_name = db.Column(db.String)



class ManagementSignUp(db.Model) :
    __tablename__='man_registration'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    password = db.Column(db.String, nullable = False)
    dob = db.Column(db.String, nullable = False)
