

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


# definr the user model 
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique = True)
    email = db.Column(db.String(80), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False, unique = True)

    books = db.relationship('UserBook', back_populates='user')

    def __init__(self, id, username, email, password):
       self.username = username
       self.id = id
       self.email = email
       self.password = password
    
    def set_password(self, password):
        return generate_password_hash(self.password, password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # represent mothod to explain how one object of this database will look like
    def __repr__(self):
        return f" Email : {self.email}, Username : {self.username }"
    
    
#define the Book model
class Books (db.Model):
    __tablename__ = 'book'
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    genre = db.Column(db.String(300), nullable=False)
    page_number = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    users = db.relationship('UserBook', back_populates='book')
    

    def __init__(self, id , title, genre, page_number, author):
        self.id = id
        self.title = title
        self.genre = genre
        self.page_number = page_number
        self.author = author
    
    def __repr__(self):
        return f"<Book {self.title}, Author: {self.author}>"

#define the user-book model
class UserBook(db.Model):
    __tablename__ = 'user_book'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)  
    book_title = db.Column(db.String(255))
    book_authors = db.Column(db.String(255))
    book_genre = db.Column(db.String(255))
    book_page_count = db.Column(db.Integer)


    user = db.relationship('User', back_populates='books')
    book = db.relationship('Books', back_populates='users')


    def __init__(self, user_id, book_id, book_title, book_authors, book_genre, book_page_count):
       self.book_id = book_id
       self.book_genre = book_genre
       self.book_authors = book_authors
       self.book_title = book_title
       self.book_page_count = book_page_count
       self.user_id = user_id
    
    def __repr__(self):
        return f"<UserBook User: {self.user_id}, Book: {self.book_title}>"