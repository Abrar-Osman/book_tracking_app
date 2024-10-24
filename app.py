
from models import User, Books, UserBook, db
import datetime
from flask import Flask, redirect, render_template, request, jsonify, url_for, flash
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
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html') 
    
    data = request.form
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    if not email or not username or not password:
         flash("email or username and password are required!!")
         return redirect (url_for('register'))
    
    if User.query.filter_by(email=email).first() or User.query.filter_by(username = username).first():
        flash('User already exists')
        return redirect (url_for('register'))
    

    hash_password = generate_password_hash(password)
    new_user = User(email = email, username = username, password = hash_password)
    
    db.session.add(new_user)
    db.session.commit()

    return  redirect(url_for('homepage'))
    
    
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html') 

    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return  flash('Missing email or password')


    email = data['email']
    password = data['password']

    user = User.query.filter_by(email = email).first()

    if not user or not check_password_hash(user.password, password):
        flash("your credential is wrong try again!")
        return redirect(url_for('login'))
    
    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=300))
 
    return  jsonify({'token' : access_token}), 200




@app.route('/search', methods=[ 'GET'])
def search_page():
    
    data = request.args
    book_name = data.get('q')
    
    if not book_name:
        flash("Invalid: the search word is required.")
        return redirect(url_for('homepage'))
  
    data = fetch_data(book_name)
    if not data:
         return flash("No books found")
    book_list = extract_book_data(data)
    store_books_in_db(book_list)
    return render_template('search.html', data=book_list)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    
    user_id = request.args.get('user_id')
    book_id = request.args.get('book_id')
    book_title = request.args.get('title')
    book_authors = request.args.get('authors')
    book_genre = request.args.get('genre')
    book_page_count = request.args.get('page_number')

   
    user_book = UserBook.query.filter_by(user_id=user_id,book_id=book_id).first()
    if user_book:
        return render_template('index.html')

    new_user_book = UserBook(
        
        user_id=user_id,
        book_id=book_id,
        book_title=book_title,
        book_authors=book_authors,
        book_genre=book_genre,
        book_page_count=book_page_count,
        
    )
        
    db.session.add(new_user_book)
    db.session.commit()

    books = UserBook.query.filter_by(user_id=user_id)
    return render_template('book_list.html', books=books)

@app.route('/book_list')
def book_list():
    try:

        return render_template('book_list.html')

    except:
        return redirect(url_for('homepage'))


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    id = request.args.get('book_id')
    user_book = UserBook.query.filter_by(id = id).first()
    db.session.delete(user_book)
    db.session.commit()

    if user_book:
        db.session.delete(user_book)
        db.session.commit()
    
    return redirect(url_for('homepage'))
    


if __name__ == '__main__':
    app.run()
