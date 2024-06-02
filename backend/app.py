from flask import Flask,send_file
from application.database import db
from application.config import SecurityConfig
from flask_restful import Api,Resource
from flask_cors import CORS
from application.security import user_datastore,security
from flask_jwt_extended import JWTManager
from application.celery_worker import make_celery
from celery.schedules import crontab
from httplib2 import Http
from json import dumps
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from application.cache import cache

# Configuration for the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.db'
db.init_app(app)
app.config.from_object(SecurityConfig)
api = Api(app)
JWTManager(app)
security.init_app(app, user_datastore)
cache.init_app(app)


CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=['GET','POST','PUT','DELETE'])
app.app_context().push()


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TIMEZONE='Asia/Kolkata'
)
celery = make_celery(app)
app.app_context().push()

@celery.task()
def add_together(a,b):
    return a+b







# Generate a .csv file
@celery.task()
def get_csv_file(category_name):
    import csv
    import os
    import time

    products = Products.query.filter_by(category = category_name).all()
    if not products:
        return None

    product_data = []
    for product in products:
        product_data.append([
            product.product_name,
            product.rate,
            product.quantity,
            product.sold,
            product.sold * product.rate
        ]) 

    with open("static/details.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Name', 'Rate', 'Available Quantity', 'Units Sold','Income from Units Sold'])
        for product in product_data:
            writer.writerow(product)

    return "Export Job Started"

class Trigger(Resource):
    def get(self, category_name):
        a = get_csv_file.delay(category_name)
        return{
            "Task_ID": a.id,
            "Task_State": a.state,
            "Task_Result": a.result
        }


class Download(Resource):
    def get(self):
        return send_file('static/details.csv', as_attachment=True)
    


@celery.on_after_finalize.connect
def daily_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=22, minute=26, day_of_month=9), SendMonthlyReport.s(), name = "2nd of every month")
    sender.add_periodic_task(crontab(hour=22, minute=26, day_of_month=9), FestiveOffers.s(), name = "Festive days")
    today = datetime.now(pytz.timezone('Asia/Kolkata')).date()
    users = Users.query.filter_by(is_admin=False).all()
    for user in users:
        orders_today = Orders.query.filter_by(username=user.username, date=today).first()
        if not orders_today:
	        sender.add_periodic_task(crontab(hour=22, minute=26), SendDailyReminder.s(), name = "Daily Evening Reminder")
		


WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAiXvYBaE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=46Bx-PE6CFOAhUk5v37H4FqoW2Soqvvc-WS338NEswI"


@celery.task()
def SendDailyReminder():
    print("Starting SendDailyReminder Task")
    url = WEBHOOK_URL
    app_message = {"text": "We have seen you haven't shopped today. Grab your groceries at the best price!!!"}
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)
    return "Reminder will be sent shortly..."
    
    


# Generate a Monthly Report

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "support@grocerio.com"
SENDER_PASSWORD = ""

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

def format_message(template_file, lastmonth, data={}, orders=[]):

    months = ["Jan", "Feb", "March", "Apr", "May", "jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    currentMonth = datetime.now().month - 1
    currentYear = datetime.now().year
    lastmonth = months[currentMonth - 1]+ "-" + str(currentYear)

    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data, lastmonth=lastmonth, orders=orders)

def get_user_orders(username, lastmonth):
    today = datetime.now(pytz.timezone('Asia/Kolkata'))
    currentMonth = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    orders = Orders.query.filter(Orders.username == username, Orders.date >= lastmonth,Orders.date < currentMonth).all()

    user_orders = []
    for order in orders:
        total_sale = order.total_sale
        address = order.address
        mode_of_payment = order.mode_of_payment
        date = order.date

        order_info = {
            'total_sale' : total_sale,
            'address' : address,
            'mode_of_payment' : mode_of_payment,
            'date' : date
        }
        user_orders.append(order_info)

    return user_orders

def send_monthly_email(data, lastmonth):
    username = data.username
    orders = get_user_orders(username, lastmonth)
    message = format_message("monthly_report.html", lastmonth = lastmonth, data = data, orders = orders)
    send_email(data.email, subject="Monthly Sale Report", message=message)

@celery.task()
def SendMonthlyReport():
    print("Starting SendMonthlyReport Task")
    users = Users.query.filter_by(is_admin = False).all()
    today = datetime.now(pytz.timezone('Asia/Kolkata'))
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    last_month = first_day_of_previous_month
    for user in users:
        send_monthly_email(data = user, lastmonth = last_month)


def send_offer_email(data, lastmonth):
    username = data.username
    orders = get_user_orders(username, lastmonth)
    message = format_message("christmas_sale.html", lastmonth = lastmonth, data = data, orders = orders)
    send_email(data.email, subject="Offer", message=message)

@celery.task()
def FestiveOffers():
    print("Starting FestiveOffers Task")
    users = Users.query.filter_by(is_admin = False).all()
    today = datetime.now(pytz.timezone('Asia/Kolkata'))
    first_day_of_current_month = today.replace(day=1, hour=0, minute=0)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    last_month = first_day_of_previous_month
    for user in users:
        send_offer_email(data = user, lastmonth = last_month)


from application.controllers import *
api.add_resource(UserSignIn,'/api/userLogin/')
api.add_resource(AdminSignIn,'/api/managementLogin/')
api.add_resource(SignUp,'/api/Registration/')
api.add_resource(ManSignUp,'/api/managementRegistration/')
api.add_resource(Product,'/api/Product/<product_name>/')
api.add_resource(ProductsList, '/api/Products/')
api.add_resource(Categories,'/api/Category/<category_name>/')
api.add_resource(CategoryList,'/api/Categories/')
api.add_resource(Search,'/api/Search/<search>/')
api.add_resource(CartList,'/api/Cart/')
api.add_resource(RequestList,'/api/Requests/')
api.add_resource(Request,'/api/Request/<request_id>/')
api.add_resource(Cart,'/api/Cart/<sale_id>/')
api.add_resource(HomePage,'/api/Home/')
api.add_resource(ManHomePage,'/api/ManHome/')
api.add_resource(Req,'/api/ManRequest/')
api.add_resource(Confirm,'/api/Confirm/')
api.add_resource(Trigger,'/api/Trigger/<category_name>')
api.add_resource(Download,'/api/Download/')
api.add_resource(SignUpRequest,'/api/SignUpRequest/<id>/')
api.add_resource(SignUpRequestList,'/api/SignUpRequests/')



if __name__ == "__main__":
    db.create_all()
    app.debug=True
    app.run(host='0.0.0.0',port=5000)
