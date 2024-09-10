from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm , LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='pic.jpg')
    email = db.Column(db.String(25), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image}")'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'User("{self.title}", "{self.date_posted}")'


posts = [
    {
        'author': 'Martin Yaney',
        'title': 'Post 1',
        'content': 'Software Engineering',
        'date_posted': 'March 05, 2022'
    },
    {
        'author': 'Will Smith',
        'title': 'Post 2',
        'content': 'Men In Black',
        'date_posted': 'March 05, 1999'
    },
    {
        'author': 'Lucy Lawless',
        'title': 'Post 3',
        'content': 'Fashion',
        'date_posted': 'December 10, 2023'
    },
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created! Username: {form.username.data}", 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f"Logged In with {form.email.data}", 'success')
            return redirect(url_for('home'))
        else:
            flash('invalid username or password', 'danger')
    return render_template('login.html',form=form)


db.create_all()
db.drop_all()
db.create_all()

user1 = User(username='John', email='john@gamil.com', password='john')
user2 = User(username='Sam', email='sam@gamil.com', password='sam')
user3 = User(username='Bill', email='bill@gamil.com', password='bill')

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

post1 = Post(title = 'POst 10', content='John first post',user_id=user1.id)
post2 = Post(title = 'POst 11', content='John second post',user_id=user1.id)
post3 = Post(title = 'POst 12', content='sam first post',user_id=user2.id)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
