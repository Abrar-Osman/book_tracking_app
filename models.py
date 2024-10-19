

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


# definr the user model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique = True)
    email = db.Column(db.String(80), nullable=False, unique = True)
    password = db.Column(db.String(80), nullable=False, unique = True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # represent mothod to explain how one object of this database will look like
    def __repr__(self):
        return f" Email : {self.email}, Username : {self.username }"
    
    
#define the Book model
class Books (db.Model):
    id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    genre = db.Column(db.String(300), nullable=False)
    page_number = db.Column(db.String(100), nullable=False)
    

#define the user-book model
class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    book_id = db.Column(db.String(100), db.ForeignKey('book.id'), nullable=False) 
    user = db.relationship('User', backref='user_books')  
    book = db.relationship('Book', backref='book_users')  
