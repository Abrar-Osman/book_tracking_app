
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

def fetch_data(book_name):
    API_KEY = 'AIzaSyAKunAimLH4KP7tBRBulOfZSYDTlPgI6rI'
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={book_name}:keyes&key={API_KEY}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return  response.json() 
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

def extract_book_data(book_data):
    books_list = []
    for book in book_data.get('items', []):
        volume_info = book.get('volumeInfo', {})
        
        title = volume_info.get('title', 'No Title')
        authors = ', '.join(volume_info.get('authors', []))  
        genre = ', '.join(volume_info.get('categories', []))  
        page_number = volume_info.get('pageCount', 'Unknown')
        book_id = book.get('id', 'Unknown')
        
        books_list.append({
            'id': book_id,
            'title': title,
            'genre': genre,
            'page_number': page_number,
            'authors': authors            
        })
    
    return books_list

def store_books_in_db(books_list):
    for book in books_list:
       
        existing_book = Books.query.filter_by(id=book['id']).first()
        
        if not existing_book:
            
            new_book = Books(
                id=book['id'],
                title=book['title'],
                genre=book['genre'],
                page_number=book['page_number'],
                author=book['authors']
            )
            
            db.session.add(new_book)
   
    db.session.commit()


@app.route('/home', methods=['POST', 'GET'])
def homepage():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        book_name = request.form.get('q')
        print(book_name)
        if book_name:  
            try:
                book_data = fetch_data(book_name)
                
                books_list = extract_book_data(book_data)
                
                redirect(url_for('search', books_list=books_list))
                # return render_template('search.html', data=books_list)
            except Exception as e:
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




@app.route('/search', methods=['GET', 'POST'])
@jwt_required()
# def search_page():
  
#   elif request.method == 'GET':
#         book_name = request.args.get('q')
  
       
#   else:
#         return jsonify({"error": "Book name is required"}), 400

# @app.route('/add_book', methods=['POST', 'GET'])
# @jwt_required()
# def add_book():
#     current_user = get_jwt_identity()  
#     user_id = current_user 

    
#     book_id = request.form.get('book_id')
#     book_title = request.form.get('book_title')
#     book_authors = request.form.get('book_authors')
#     book_genre = request.form.get('book_genre')
#     book_page_count = request.form.get('book_page_count')

   
#     user_book = UserBook.query.filter_by(user_id=user_id, book_id=book_id).first()
#     if user_book:
#         return jsonify({'message': 'Book already in your list'}), 400

 
#     new_user_book = UserBook(
        
#         id = id,
#         user_id=user_id,
#         book_id=book_id,
#         book_title=book_title,
#         book_authors=book_authors,
#         book_genre=book_genre,
#         book_page_count=book_page_count,
        
#     )
    
#     db.session.add(new_user_book)
#     db.session.commit()

#     return jsonify({'message': 'Book added to your list successfully'}), 201





if __name__ == '__main__':
    app.run()
