import secrets
import jwt
from functools import wraps
from application.model import *
from sqlalchemy import func
from datetime import datetime,timedelta
from flask import jsonify,session
from flask_restful import Resource,reqparse
from flask_security.utils import hash_password,verify_password
from flask_security import login_user
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from application.cache import cache
from application.cache_api import *


# Controller for User Login page
class UserSignIn(Resource) : 
    def post(self) : 
        loginParser = reqparse.RequestParser()
        loginParser.add_argument('username', type = str, required = True)
        loginParser.add_argument('password', type = str, required = True)
        args = loginParser.parse_args()
        username = args.get('username',None)
        password = args.get('password',None)
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            if not user.is_admin:
                if verify_password(password, user.password)  and user.role == 'user':
                    access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(seconds=1200))
                    login_user(user)
                    user.active = True
                    db.session.commit()
                    return {'SignIn': 'Successful','access_token' : access_token, 'username' : username},200
                else:
                    return {'SignIn': 'Failed'},400
            else:
                return {'SignIn': 'Failed'},406
        else:
            return {'SignIn': 'Failed'},402
        
    def user_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()

            user_id = get_jwt_identity()
            user = Users.query.get(user_id) 

            if not user or user.is_admin:
                return jsonify(message="User required"), 403

            return func(*args, **kwargs)

        return decorated_function
            



# Controller for Management Login page
class AdminSignIn(Resource):
    def post(self):
        loginParser = reqparse.RequestParser()
        loginParser.add_argument('username', type = str, required = True)
        loginParser.add_argument('password', type = str, required = True)
        args = loginParser.parse_args()
        username = args.get('username',None)
        password = args.get('password',None)
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            if user.is_admin:
                if verify_password(password, user.password)  and user.role in ['management','admin']:
                    access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(seconds=1200))
                    login_user(user)
                    user.active = True
                    if user.role == 'admin':
                        return {'SignIn': 'Successful','access_token' : access_token, 'username' : username, 'role' : 'admin'},200
                    else:
                        return {'SignIn': 'Successful','access_token' : access_token, 'username' : username, 'role' : 'management'},200
                else:
                    return {'SignIn': 'Failed'},400
            else:
                return {'SignIn': 'Failed'},406
        else:
            return {'SignIn': 'Failed'},404
        
    def admin_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()  

            user_id = get_jwt_identity() 
            user = Users.query.get(user_id)

            if not user or not user.is_admin:
                return jsonify(message="Admin permissions required"), 403

            return func(*args, **kwargs)

        return decorated_function


# Controller for User Registration Page
class SignUp(Resource):
    def post(self):
        registerParser = reqparse.RequestParser()
        registerParser.add_argument('first_name', type = str, required = True)
        registerParser.add_argument('last_name', type = str)
        registerParser.add_argument('username', type = str, required = True)
        registerParser.add_argument('password', type = str, required = True)
        registerParser.add_argument('email', type = str, required = True)
        registerParser.add_argument('dob', type = str, required = True)
        args = registerParser.parse_args()
        fname = args.get('first_name',None)
        lname = args.get('last_name',None)
        username = args.get('username',None)
        password = args.get('password',None)
        email = args.get('email',None)
        dob = args.get('dob',None)
        try : 
            user=Users(first_name=fname,last_name=lname,username=username,password=hash_password(password),email=email,dob=dob,active=False,is_admin=False,role='user')
            user.fs_uniquifier = secrets.token_hex(16)
            db.session.add(user)
            db.session.commit()
        except :
            db.session.rollback()
            return {'SignUp' : 'Failed'},406
        return {'SignUp' : 'Successful'},200
        



# Controller for Management Registration Page
class ManSignUp(Resource):
    def post(self):
        registerParser = reqparse.RequestParser()
        registerParser.add_argument('first_name', type = str, required = True)
        registerParser.add_argument('last_name', type = str)
        registerParser.add_argument('username', type = str, required = True)
        registerParser.add_argument('password', type = str, required = True)
        registerParser.add_argument('email', type = str, required = True)
        registerParser.add_argument('dob', type = str, required = True)
        args = registerParser.parse_args()
        fname = args.get('first_name',None)
        lname = args.get('last_name',None)
        username = args.get('username',None)
        password = args.get('password',None)
        email = args.get('email',None)
        dob = args.get('dob',None)
        try : 
            request=ManagementSignUp(first_name=fname,last_name=lname,username=username,password=hash_password(password),email=email,dob=dob)
            # user.fs_uniquifier = secrets.token_hex(16) active=False,is_admin=True,role='management'
            db.session.add(request)
            db.session.commit()
        except :
            db.session.rollback()
            return {'SignUp' : 'Failed'},406
        return {'SignUp' : 'Successful'},200
    

# Controller for approving and deleting the signup requests
class SignUpRequest(Resource):
    @jwt_required()
    @AdminSignIn.admin_required
    def post(self,id):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        request = ManagementSignUp.query.filter_by(id = id).first()
        try:
            if request : 
                man_user=Users(first_name=request.first_name,last_name=request.last_name,username=request.username,password=request.password,email=request.email,dob=request.dob, active=False,is_admin=True,role='management')
                man_user.fs_uniquifier = secrets.token_hex(16) 
                db.session.add(man_user)
                db.session.delete(request)
                db.session.commit()
                return {'msg' : 'Successful'}, 200
            else:
                return {'msg' : 'Failed'}, 400
        except:
            db.session.rollback()
            return {'msg' : 'Failed'}, 400
    
    @jwt_required()
    @AdminSignIn.admin_required
    def delete(self,id):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        request = ManagementSignUp.query.filter_by(id = id).first()
        try:
            if request : 
                db.session.delete(request)
                db.session.commit()
                return {'msg' : 'Successful'}, 200
            else:
                return {'msg' : 'Failed'}, 400
        except:
            db.session.rollback()
            return {'msg' : 'Failed'}, 400



# Controller for signup request list
class SignUpRequestList(Resource):
    @jwt_required()
    @AdminSignIn.admin_required
    def get(self) :
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        requests = ManagementSignUp.query.all()
        if requests : 
            result = [{'name' : request.username,
                        'first_name' : request.first_name,
                        'last_name' : request.last_name,
                        'password' : request.password,
                        'id' : request.id,
                        'email' : request.email,
                        'dob' : request.dob} for request in requests]
            return {'result' : result,'msg' : 'Success','user' : user.first_name},200
        else:
            return {'msg' : 'Failed', 'user' : user.first_name},404
        




# Controller for Home page
class HomePage(Resource):
    @jwt_required()
    @UserSignIn.user_required
    def get(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        store_data = get_products_from_categories()
        return {"result" : store_data, "name" : user.first_name}, 200




 

# Controller for Search bar
class Search(Resource) : 
    @jwt_required()
    @UserSignIn.user_required
    def get(self,search):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        try :
            result = Products.query.filter(Products.product_name.ilike("%"+search+"%")).all()
            if result : 
                results = [{'product_name' : r.product_name,
                                'unit' : r.unit,
                                'rate' : r.rate,
                                'quantity' : r.quantity,
                                'category' : r.category} for r in result]
                return {'msg': 'Success','results' : results, 'type' : 'Product', 'user' : user.first_name},200
            else:
                category = Category.query.filter(Category.category_name.ilike("%"+search+"%")).all()
                if category : 
                    items = {'items': []}
                    categories = [item.category_name for item in category]
                    for category in categories : 
                        products = Products.query.filter_by(category = category).all()
                        if products : 
                            items['items'].append({
                                'name' : category,
                                'products' : [{'product_name' : product.product_name,
                                                'unit' : product.unit,
                                                'rate' : product.rate,
                                                'quantity' : product.quantity,
                                                'category' : product.category} for product in products]
                            }) 
                    return {'msg': 'Success','results' : items, 'type' : 'Category', 'user' : user.first_name}, 200
                else : 
                    return {'msg' : 'No Such Product Found' ,'user' : user.first_name}, 200
        except : 
                return {'msg' : 'Search Failed'}
    



# Controller for Find, Update & Delete a Product
class Product(Resource) : 

    @jwt_required()
    @AdminSignIn.admin_required
    def get(self,product_name) :
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        product = get_product(product_name)
        if product : 
            return {'result' : {'name' : product.product_name, 'unit' : product.unit, 'rate' : product.rate, 'quantity' : product.quantity, 'category' : product.category}, 'msg' : 'Success', 'name' : user.first_name}, 200
        else :
            return {'msg' : 'Failed'}, 404
        
    
    @jwt_required()
    @AdminSignIn.admin_required
    def put(self,product_name) :
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        product = get_product(product_name)
        if product : 
            productParser = reqparse.RequestParser()
            productParser.add_argument('product_name', type = str)
            productParser.add_argument('unit', type = str)
            productParser.add_argument('rate', type = float)
            productParser.add_argument('quantity', type = float) 
            args = productParser.parse_args()
            pname = args.get('product_name', product.product_name)
            unit = args.get('unit', product.unit)
            rate = args.get('rate', product.rate)
            quantity = args.get('quantity', product.quantity)
            product.product_name = pname
            product.unit = unit
            product.rate = rate
            product.quantity = quantity
            db.session.commit()
            return {'msg' : 'Successful'},200
        else:
            db.session.rollback()
            return {'msg' : 'Falied'},404
        
    
    @jwt_required()
    @AdminSignIn.admin_required
    def delete(self,product_name) : 
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        product = get_product(product_name)
        if product : 
            db.session.delete(product)
            db.session.commit()
            return {'msg' : 'Successful'},200
        else : 
            db.session.rollback()
            return {'msg' : 'Product Not Found'},404
        


# Controller for Adding a product or finding a list of products 
class ProductsList(Resource):
    
    def get(self) : 
        
        products = get_all_products()
        if products : 
            product_list = [{'name' : product.product_name, 'unit' : product.unit, 'rate' : product.rate, 'quantity' : product.quantity, 'category' : product.category} for product in products]
            return {'result' : product_list}, 200
        else : 
            return {'result' : [], 'msg' : 'Category Not Found / No products available'}, 404
        
    
    def post(self) : 
            productParser = reqparse.RequestParser()
            productParser.add_argument('product_name', type = str, required = True)
            productParser.add_argument('unit', type = str, required = True)
            productParser.add_argument('rate', type = float, required = True)
            productParser.add_argument('quantity', type = float, required = True) 
            productParser.add_argument('category_name', type = str, required = True) 
            args = productParser.parse_args()
            pname = args.get('product_name', None)
            unit = args.get('unit', None)
            rate = args.get('rate', None)
            quantity = args.get('quantity', None)
            category_name = args.get('category_name', None)
            try : 
                product = Products(product_name = pname, unit = unit, rate = rate, quantity = quantity, category = category_name, sold = 0)
                db.session.add(product)
                db.session.commit()
            except :
                db.session.rollback()
                return {'msg' : 'Failed'},406
            return {'msg' : 'Successful'},200
        
         



# Controller for Finding, Updating and Deleting a Category
class Categories(Resource) : 
    
    def get(self,category_name) : 
        
        category = get_category(category_name)
        if category : 
            return jsonify({'msg' : 'Category Found'}, 200)
        else : 
            return jsonify({'msg' : 'Category Not Found'}, 404)
        
    
    def put(self,category_name) : 
            category = get_category(category_name)
            if category : 
                categoryParser = reqparse.RequestParser()
                categoryParser.add_argument('name', type=str, required = True)
                args = categoryParser.parse_args()
                cat_name = args.get('name',category_name)
                category.category_name = cat_name
                db.session.commit()
                return jsonify({'msg' : 'Category Updated Successfully'},200)
            else:
                return jsonify({'msg' : 'Category Not Found'},404)
        
    
    
    def delete(self,category_name):
            category = get_category(category_name)
            if category :     
                db.session.delete(category)
                db.session.commit()
                return {'msg' : 'Successful'},200
            else : 
                return{'msg' : 'Failed'},404
        





# Controller for New Category
class CategoryList(Resource) :
    def get(self):
        categories = get_all_categories()
        if categories : 
            result = [{'name' : category.category_name} for category in categories]
            return {'result' : result}, 200
        else : 
            return {'result' : [], 'msg' : 'No categories are currently present'}, 404
        
    
    def post(self):
            categoryParser = reqparse.RequestParser()
            categoryParser.add_argument('name', type = str, required = True )
            args = categoryParser.parse_args()
            cname = args.get('name', None)
            try : 
                category = Category(category_name = cname)
                db.session.add(category)
                db.session.commit()
            except : 
                db.session.rollback()
                return {'msg' : 'Failed'},406
            return {'msg' : 'Successful'},200
        



# Controller for getting list of requests & adding a new request
class RequestList(Resource) : 
    @jwt_required()
    @AdminSignIn.admin_required
    def get(self) :
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        requests = Requests.query.all()
        if requests : 
            result = [{'type' : request.type,
                        'old_name' : request.old_name,
                        'by' : request.by,
                        'date' : request.date,
                        'id' : request.request_id,
                        'new_name' : request.new_name} for request in requests]
            return {'result' : result,'msg' : 'Success','user' : user.first_name},200
        else:
            return {'msg' : 'Failed', 'user' : user.first_name},404
        
    
    @jwt_required()
    @AdminSignIn.admin_required
    def post(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        requestParser = reqparse.RequestParser()
        requestParser.add_argument('type', type = str, required = True)
        requestParser.add_argument('old_name', type = str)
        requestParser.add_argument('new_name', type = str)
        args = requestParser.parse_args()
        type = args.get('type',None)
        old_name = args.get('old_name',None)
        new_name = args.get('new_name',None)
        try:
            request = Requests(type = type, new_name = new_name, old_name = old_name, by = user.username, date = datetime.now().date())
            db.session.add(request)
            db.session.commit()
        except:
            db.session.rollback()
            return {'msg' : 'Failed'}
        return {'msg' : 'Successful'}, 200
        
        


# Controller for deleting,updating and fetching a particular request
class Request(Resource):
    def get(self,request_id): 
        request = Requests.query.filter_by(request_id = request_id).first()
        if request:
            return {'msg' : 'Request Found Successfully'},200
        return {'msg' : 'Request not Found'}, 404
        
    @jwt_required()
    @AdminSignIn.admin_required
    def put(self,request_id):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        request = Requests.query.filter_by(request_id = request_id).first()
        try:
            if request : 
                category = Category.query.filter_by(category_name = request.old_name).first()
                products = Products.query.filter_by(category = request.old_name).all()
                for product in products:
                    product.category = request.new_name
                category.category_name = request.new_name
                db.session.delete(request)
                db.session.commit()
                return {'msg' : 'Successful'}, 200
            return {'msg' : 'Failed'}, 400
        except:
            db.session.rollback()
            return {'msg' : 'Failed'}, 400
        

    @jwt_required()
    @AdminSignIn.admin_required
    def post(self,request_id):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        request = Requests.query.filter_by(request_id = request_id).first()
        try:
            if request : 
                category = Category(category_name = request.new_name)
                db.session.add(category)
                db.session.delete(request)
                db.session.commit()
                return {'msg' : 'Successful'}, 200
            else:
                return {'msg' : 'Failed'}, 400
        except:
            db.session.rollback()
            return {'msg' : 'Failed'}, 400
    
    @jwt_required()
    @AdminSignIn.admin_required
    def delete(self,request_id):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        request = Requests.query.filter_by(request_id = request_id).first()
        try:
            if request : 
                db.session.delete(request)
                db.session.commit()
                return {'msg' : 'Successful'}, 200
            else:
                return {'msg' : 'Failed'}, 400
        except:
            db.session.rollback()
            return {'msg' : 'Failed'}, 400
        

# Controller for Listing the cart
class CartList(Resource) : 
    @jwt_required()
    @UserSignIn.user_required
    def get(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        sale=Sale.query.filter_by(username=user.username).all()
        if sale :
            total=db.session.query(func.sum(Sale.cost)).filter(Sale.username==user.username).scalar()
            sales = [{'id' : s.sale_id,
                        'product' : s.product,
                        'quantity' : s.quantity,
                        'rate' : s.rate,
                        'cost' : s.cost} for s in sale]
            return {'items' : sales, 'total_cost' : total},200
        else : 
            return {'msg' : 'No Sale Done Yet'}, 404
            

    # Controller for Add to Cart
    @jwt_required()
    @UserSignIn.user_required
    def post(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        saleParser = reqparse.RequestParser()
        saleParser.add_argument('product', type = str, required = True)
        saleParser.add_argument('quantity', type = float, required = True)
        args = saleParser.parse_args()
        product_name = args.get('product', None)
        quantity = args.get('quantity', None)
        products = get_product(product_name)
        if quantity > 0 and quantity <= products.quantity:
            try : 
                product = Sale.query.filter_by(product = product_name,username=user.username).first()
                if product is None :
                    sale = Sale(product = product_name, quantity = quantity, rate = products.rate, username = user.username, cost = products.rate*quantity)
                    db.session.add(sale)
                else :
                    if product.quantity + quantity < products.quantity:
                        product.quantity += quantity
                        product.cost += products.rate*quantity
                    else:
                        return {'msg' : 'Invalid'}, 200
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")
                return {'msg' : 'Fail', 'error' : str(e)}, 406
            return  {'msg' : 'Success'}, 200
        else :
            return {'msg' : 'Fail'}, 400
    
        


# Controller for modifying and deleting a purchase in the cart
class Cart(Resource) :
    def get(self,sale_id) : 
        sale=Sale.query.filter_by(sale_id=sale_id).first()
        if sale : 
            return jsonify({'msg' : 'Product Found Successfully'}, 200)
        return jsonify({'msg' : 'Sale not found'}, 404)
    
    
    def put(self, sale_id) : 
            sale=Sale.query.filter_by(sale_id=sale_id).first()
            cartParser = reqparse.RequestParser()
            cartParser.add_argument('quantity', type = float, required = True)
            args = cartParser.parse_args()
            quantity = args.get('quantity', sale.quantity)
            try : 
                sale = Sale(username = sale.username, product = sale.product, quantity = quantity, rate = sale.rate, cost = quantity*sale.rate)
                db.session.add(sale)
                db.session.commit()
            except : 
                db.session.rollback()
                return {'msg' : 'Update Unsuccessful'}, 406
            return {'msg' : 'Update Successful'}, 200
            
        
    @jwt_required()
    @UserSignIn.user_required
    def delete(self,sale_id) : 
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        try:
            sale=Sale.query.filter_by(sale_id=sale_id).first()
            if sale : 
                db.session.delete(sale)
                db.session.commit()
                return {'msg' : 'Success'},200
            else:
                db.session.rollback()
                return {'msg' : 'Fail'},404
        except Exception as e:
            return {'msg' : 'Failed','error' : e},406
            
      



# Controller for Confirmation Page
class Confirm(Resource):
    @jwt_required()
    @UserSignIn.user_required
    def get(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        total = db.session.query(func.sum(Sale.cost)).filter(Sale.username==user.username).scalar()
        return {'total' : total, "user": user.first_name}


    @jwt_required()
    @UserSignIn.user_required
    def post(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        orderParser = reqparse.RequestParser()
        orderParser.add_argument('address', type = str, required = True)
        orderParser.add_argument('mop', type = str, required = True)
        args = orderParser.parse_args()
        address = args.get('address', None)
        mop = args.get('mop', None)
        try :
            total = db.session.query(func.sum(Sale.cost)).filter(Sale.username==user.username).scalar()
            order = Orders(username=user.username,total_sale=total,address=address,mode_of_payment=mop,date=datetime.now().date())
            db.session.add(order)
            sale = Sale.query.filter_by(username=user.username).all()
            for i in sale:
                product = Products.query.filter_by(product_name=i.product).first()
                product.quantity = product.quantity - i.quantity
                product.sold = product.sold + i.quantity
                db.session.delete(i)
            db.session.commit()
        except Exception as e :
            db.session.rollback()
            return {'msg' : 'Order Unsuccessful', 'error' : str(e)}, 406
        return {'msg' : 'Order Successful'}, 200


  


# Management homePage
class ManHomePage(Resource):
    @jwt_required()
    @AdminSignIn.admin_required
    def get(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        store_data = get_products_from_categories()
        return {"result" : store_data, "name" : user.first_name}, 200



# Controller for getting User specific Requests
class Req(Resource):
    @jwt_required()
    @AdminSignIn.admin_required
    def get(self):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        requests = Requests.query.filter_by(by = user.username).all()
        if requests : 
            result = [{'type' : request.type,
                        'old_name' : request.old_name,
                        'by' : request.by,
                        'date' : request.date,
                        'id' : request.request_id,
                        'new_name' : request.new_name} for request in requests]
            return {'result' : result,'msg' : 'Success','user' : user.first_name},200
        else:
            return {'msg' : 'Failed', 'user' : user.first_name},404
        


