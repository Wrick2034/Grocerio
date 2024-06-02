from flask_security import SQLAlchemyUserDatastore,Security
from application.database import db
from application.model import Users, Role

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security()