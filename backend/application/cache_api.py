from application.cache import cache
from application.model import *
from flask_jwt_extended import jwt_required


@jwt_required()
@cache.memoize(10)
def get_products_from_categories():
    categories = Category.query.all()
    store_data = {"items" : []}
    for category in categories : 
        products = Products.query.filter_by(category=category.category_name).all()
        store_data["items"].append({
               "name" : category.category_name,
               "products" : [{'product_name' : product.product_name,
                                'unit' : product.unit,
                                'rate' : product.rate,
                                'quantity' : product.quantity,
                                'category' : product.category} for product in products]
                })
    return store_data


@jwt_required()
@cache.memoize(10)
def get_product(product_name):
    product = Products.query.filter_by(product_name = product_name).first()
    return product
    

@jwt_required()
@cache.memoize(10)
def get_all_products():
    product = Products.query.all()
    return product

@jwt_required()
@cache.memoize(10)
def get_category(category_name):
    category = Category.query.filter_by(category_name = category_name).first()
    return category


@jwt_required()
@cache.memoize(10)
def get_all_categories():
    category = Category.query.all()
    return category
