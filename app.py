
from models import User, Books, UserBook, db
import datetime
from flask import Flask, redirect, render_template, request, jsonify, url_for
from dotenv import load_dotenv
import os
from flask_migrate import Migrate, migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests


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
db.init_app(app)
migrate = Migrate(app, db)
Jwt = JWTManager(app)


# this line solve the issues that the db cant run without the app_context method
with app.app_context():
    db.create_all() 


# function to manage authorization to the routes that need one
# def required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         token = None
        
#     # check the presence of the  jwt token in the request header
#         if 'Authorization' in request.header:
#             auth_header = request.headers['authorization']
#             token = auth_header.split(" ")[1] if len(auth_header.split(" ")) == 2 else None    
#         if not 'Authorization':
#             return jsonify({'message' : 'Token is missing!!'}), 401
        
#     # encode the token    
#         try:
#             data = Jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#             current_user = User.query.filter_by(id = data['id']).first()
#             if not current_user:
#                 return jsonify({'message' : 'User not found!!'}), 401
            
#     # check if the its expired and is valid
#         except Jwt.expiredSignatureError:
#             return jsonify({'message' : 'Token is expired!!'}), 401
#         except Jwt.InvalidTokenError:
#             return jsonify({'message', 'Token is invalid!!'}), 401
        
#         return func(current_user, *args, **kwargs)
#     return decorated



@app.route('/home', methods=['POST', 'GET'])
def homepage():
    return render_template('index.html')



@app.route('/', methods=['POST', 'GET'])
def welcome():
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html') 
    
    data = request.form
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    if not email or not username or not password:
        return jsonify({'message' : 'email or username and password are required!!'}), 400
    
    
    if User.query.filter_by(email=email).first() or User.query.filter_by(username = username).first():
        return jsonify({'message' : 'User already exist!!'}), 400
    

    hash_password = generate_password_hash(password)
    new_user = User(email = email, username = username, password = hash_password)
    
    db.session.add(new_user)
    db.session.commit()

    return  redirect(url_for('homepage'))
    
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html') 

    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"msg": "Missing email or password"}), 400


    email = data['email']
    password = data['password']

    user = User.query.filter_by(email = email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message' : 'Wrong Credintioal!!'}), 401
    
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=300))
 
    return  jsonify({'token' : access_token}), 200


@app.route('/search', methods=['POST','GET'])
@jwt_required()
def search_page():
    current_user = get_jwt_identity()  
    search_query = request.form.get('query')
    
    if not search_query:
        return 'please profide a book name', 400
    
    API_KEY = 'AIzaSyAKunAimLH4KP7tBRBulOfZSYDTlPgI6rI'
    api_url = f'https://www.googleapis.com/books/v1/volumes?q={search_query}&key={API_KEY}'
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
#         books = data.get('items', [])
        
#         book_list =[]
#         for book in books:
#             book_info = book.get('volumeInfo', {})
#             book_title = book_info.get('title', 'No Title')
#             authors = ', '.join(book_info.get('authors', ['Unknown Author']))  
#             genre = ', '.join(book_info.get('categories', ['Unknown Genre']))  
#             page_count = book_info.get('pageCount', 'N/A')

# # Add the extracted data to the list
#             book_list.append({
#                     'id': book['id'],
#                     'title': book_title,
#                     'authors': authors,
#                     'genre': genre,
#                     'page_count': page_count
#                  })
        return render_template('search.html', data=data, query=search_query)
    
    else:
        return f"Error fetching results from Google Books API: {response.status_code}", 500

# @app.route('/add_book', methods=['POST'])
# @jwt_required()
# def add_book():
#     current_user = get_jwt_identity()  
#     user_id = current_user['id']  


#     book_id = request.form.get('book_id')
#     book_title = request.form.get('book_title')
#     book_authors = request.form.get('book_authors')
#     book_genre = request.form.get('book_genre')
#     book_page_count = request.form.get('book_page_count')

   
#     user_book = UserBook.query.filter_by(user_id=user_id, book_id=book_id).first()
#     if user_book:
#         return jsonify({'message': 'Book already in your list'}), 400

 
#     new_user_book = UserBook(
    
#         book_id=book_id,
#         book_genre=book_genre,
#         book_authors=book_authors,
#         book_title=book_title,
#         book_page_count=book_page_count,
#          user_id=user_id

#     )
    
#     db.session.add(new_user_book)
#     db.session.commit()

#     return jsonify({'message': 'Book added to your list successfully'}), 201





if __name__ == '__main__':
    app.run()
