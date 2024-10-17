

from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_migrate import Migrate, migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


# load the dotenv file
load_dotenv()

# intitlize the flask application
app = Flask(__name__)


# configration the app with set value from the enviroment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', default=False)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')


# intializing the extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Jwt = JWTManager(app)

# definr the user model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique = True)
    email = db.Column(db.String(80), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False, unique = True)

    # represent mothod to explain how one object of this database will look like
    def __repr__(self):
        return f" Email : {self.email}, Username : {self.username }"

# this line solve the issues that the db cant run without the app_context method
with app.app_context():
    db.create_all() 

# function to generate the html pages
def get_html(page_name):
    html_page = open(page_name + '.html')
    content = html_page.read()
    html_page.close()
    return content


# function to manage authorization to the routes that need one
def required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        
    # check the presence of the  jwt token in the request header
        if 'Authorization' in request.header:
            auth_header = request.headers['authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) == 2 else None    
        if not 'Authorization':
            return jsonify({'message' : 'Token is missing!!'}), 401
        
    # encode the token    
        try:
            data = Jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id = data['id']).first()
            if not current_user:
                return jsonify({'message' : 'User not found!!'}), 401
            
    # check if the its expired and is valid
        except Jwt.expiredSignatureError:
            return jsonify({'message' : 'Token is expired!!'}), 401
        except Jwt.InvalidTokenError:
            return jsonify({'message', 'Token is invalid!!'}), 401
        
        return func(current_user, *args, **kwargs)
    return decorated



@app.route('/register', methods=['POST'])
def register():
    
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email = email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message' : 'Wrong Credintioal!!'}), 401
    access_token = create_access_token(identity=user.id)









if __name__ == '__main__':
    app.run()
