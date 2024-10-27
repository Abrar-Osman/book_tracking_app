
from models import User, Books, UserBook, db
from flask import Flask, redirect, render_template, request, jsonify, url_for, flash
from dotenv import load_dotenv
import os
from flask_migrate import Migrate, migrate
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from flask_login import login_user,LoginManager,current_user,logout_user,login_required,login_manager
import json



# load the dotenv file
load_dotenv()

# intitlize the flask application
app = Flask(__name__)


# configration the app with set value from the enviroment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', default=False)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')




# intializing the extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'login'

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
@login_required
def homepage():   
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int (user_id))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html') 
    
    data = request.form
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    
    if not email or not username or not password:
         flash("email or username and password are required!!", "error")
         return redirect (url_for('register'))
    
    if User.query.filter_by(email=email).first() or User.query.filter_by(username = username).first():
        flash('User already exists', "error")
        return redirect (url_for('register'))
    

    hash_password = generate_password_hash(password)
    new_user = User( email = email, username = username, password = hash_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    flash("welcome on board!!", "success")
    return  redirect(url_for('login'))
    
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html') 

    data = request.form
    if not data or 'email' not in data or 'password' not in data:
        flash('Missing email or password', "error")
        return redirect(url_for(login))

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email = email).first()
    

    if not user or not check_password_hash(user.password, password):
        flash("your credential is wrong try again!", "error")
        return redirect(url_for('login'))
    
    login_user(user)
    flash("welcome back!!", "success")
    return redirect(url_for("homepage"))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        
        
        if not new_username or not new_email:
            flash("All fields are required.", "error")
            return redirect(url_for('update_profile'))
        
        if User.query.filter_by(email=new_email).first() or User.query.filter_by(username = new_username).first():
            flash('User already exists', "error")
            return redirect (url_for('profile'))
        
        current_user.username = new_username
        current_user.email = new_email
        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating your profile.", "error")
            
        return redirect(url_for('homepage'))
    return render_template('profile.html')

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/search', methods=[ 'GET'])
@login_required
def search_page():
    
    data = request.args
    book_name = data.get('q')
    
    if not book_name:
        flash("Invalid: the search word is required.", "error")
        return redirect(url_for('homepage'))
  
    data = fetch_data(book_name)
    if not data:
        flash("No books found", "error")
        return redirect(url_for('homepage')) 
    
    book_list = extract_book_data(data)
    store_books_in_db(book_list)
    return render_template('search.html', data=book_list)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    
    user_id = current_user.id
    book_id = request.args.get('book_id')
    book_title = request.args.get('title')
    book_authors = request.args.get('authors')
    book_genre = request.args.get('genre')
    book_page_count = request.args.get('page_number')

   
    user_book = UserBook.query.filter_by(user_id=user_id,book_id=book_id).first()
    if user_book:
        flash('The book already in your booklist', "error")
        return redirect(url_for('book_list'))

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
    
    flash('you added the book successfuly',  "success")
    return redirect(url_for('homepage'))

@app.route('/book_list')
@login_required
def book_list():
    try:
        user_id = current_user.id
        books = UserBook.query.filter_by(user_id=user_id)
        return render_template('book_list.html', books=books)
    
    except:
        return redirect(url_for('homepage'))


@app.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    id = request.args.get('book_id')
    user_book = UserBook.query.filter_by(id = id).first()
    db.session.delete(user_book)
    db.session.commit()

    if user_book:
        db.session.delete(user_book)
        db.session.commit()
    
    return redirect(url_for('homepage'))


@app.route('/add_user_picks', methods=['GET', 'POST'])
@login_required
def user_picks():
    id = request.args.get('book_id') 
    title = request.args.get('book_title')
    
    book ={
        'id' : id,
        'title' : title  
    }  
    
    
    with open('user_picks.json', 'r+') as read_list:
        reading_list = json.load(read_list)
        
        for existing_book in reading_list.get("reading", []):
            if existing_book['id'] == id:
                flash('This book already in your reading books list', "error")
                return redirect(url_for('book_list'))
        
        reading_list["reading"].append(book)
        read_list.seek(0)
        json.dump(reading_list, read_list, indent = 4)

    flash('added successfully to the reading list',  "success")
    return redirect(url_for('homepage'))

@app.route('/user_picks')
@login_required
def user_picks_display():
  with open('user_picks.json', 'r') as data:
      book = json.load(data)
      return render_template('user_picks.html', data=book)  
    
if __name__ == '__main__':
    app.run()
