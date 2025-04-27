from functools import wraps
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, Text
from flask_bootstrap import Bootstrap5
import datetime as dt
import os

#TODO GOOGLE MAPS API TO SHOW THE CAFE ON A MAP ON ITS PAGE

app = Flask(__name__)

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap5(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

# Admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function

# CREATE DB
class Base(DeclarativeBase):
    pass

# Connect to Database
app.config['SECRET_KEY'] = 'OhjJK&fs3rfX1!af£4dsg%)Gsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Tables init with relative references
# Cafe table init
class Cafe(db.Model):
    __tablename__ = "cafes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Key "users.id" the users refers to the tablename of User.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    # Reference to the User object with "posts" in the User class.
    author = relationship("User", back_populates="posts")
    # Parent relationship to the comments
    comments = relationship("Comment", back_populates="parent_post")

    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    # In case I want to use it as an API, so I can get values and then use them to make a json file
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# User table init
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # This will act like a list of cafes objects attached to each User.
    # Parent relationship with "author" in the Cafe class.
    posts = relationship("Cafe", back_populates="author")
    # Parent relationship with "comment_author" in the Comment class.
    comments = relationship("Comment", back_populates="comment_author")

    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

# Comment table init
class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Child relationship with "comments" in the User class.
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    # Child Relationship to the Cafe
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("cafes.id"))
    parent_post = relationship("Cafe", back_populates="comments")

    text: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

def get_db_list(model):
    with app.app_context():
        results = db.session.query(model).all()
    return [item.as_dict() for item in results]


#TODO MULTIPAGE (10 ITEMS PER PAGE), IN HTML USE [(INDEX OF THE PAGE-1)*10+1:10*INDEX OF THE PAGE] FOR THE INDEX OF THE PAGE THOU, HOW DO i MAKE IT? /HOME/<INDEX>?
#--------------------------------------------- HOMEPAGE ----------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', cafe_list=get_db_list(Cafe), date=dt.datetime.today().year)

#------------------------------------------------- LOGIN -------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = request.form
        with app.app_context():
            result = db.session.execute(db.select(User).where(User.email == form['email']))
            user = result.scalar()
            if not user:
                flash("That email does not exist, please try again.")
                return redirect(url_for('login'))
            # Password incorrect
            elif not check_password_hash(user.password, form['password']):
                flash('Password incorrect, please try again.')
                return redirect(url_for('login'))
            else:
                login_user(user)
                return redirect(url_for('home'))

    return render_template('login.html', date=dt.datetime.today().year, current_user=current_user)

#--------------------------------------------- REGISTER ----------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        if form['password'] == form['confirm_password']:
            with app.app_context():
                # Check if user email is already present in the database.
                result = db.session.execute(db.select(User).where(User.email == form['email']))
                user = result.scalar()
                if user:
                    # User already exists
                    # flash("You've already signed up with that email, log in instead!")
                    return redirect(url_for('login'))

                hash_and_salted_password = generate_password_hash(
                    form['password'],
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                new_user = User(
                    email=form['email'],
                    name=form['name'],
                    password=hash_and_salted_password,
                )
                db.session.add(new_user)
                db.session.commit()
                # This line will authenticate the user with Flask-Login
                login_user(new_user)
                return redirect(url_for('home'))
    return render_template('register.html', date=dt.datetime.today().year, current_user=current_user)

#--------------------------------------------- LOGOUT ----------------------------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#--------------------------------------------- NEW POST ----------------------------------------------
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        pass
    return  render_template('new-cafe.html', current_user=current_user, date=dt.datetime.today().year)

#--------------------------------------------- EDIT POST ----------------------------------------------
@app.route('/edit/<_id>', methods=['GET', 'POST'])
def edit(_id):
    with app.app_context():
        result = db.session.execute(db.select(Cafe).where(Cafe.id == _id))
        cafe = result.scalar()
    if request.method == 'POST':
        pass
    return render_template('edit-cafe.html', current_user=current_user, date=dt.datetime.today().year, cafe=cafe)

#--------------------------------------------- DELETE POST ----------------------------------------------
@app.route('/delete/<_id>')
def delete(_id):
    with app.app_context():
        result = db.session.execute(db.select(Cafe).where(Cafe.id == _id))
        cafe = result.scalar()
        db.session.delete(cafe)
        print('removed item: ', _id)
        # db.session.commit() !!! TO UNCOMMENT BEFORE RELEASE <------------ !!!
    return redirect(url_for('home'))

#MAYBE I DON'T ACTUALLY NEED TO MAKE A POST PAGE
@app.route('/post/<post_id>')
def post():
    return  render_template('post.html', date=dt.datetime.today().year, current_user=current_user)

if __name__ == '__main__':
    app.run(debug=True)