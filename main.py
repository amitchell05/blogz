from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:holi!f4me@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'wTq2aV3ssbqsvaSW'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index', 'signup']
    print(session)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_error = ""
    password_error = ""
    verify_error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if not no_spaces(username) or is_empty(username) or not valid_len(username):
            username_error = "Enter a valid username"

        if not no_spaces(password) or is_empty(password) or not valid_len(password):
            password_error = "Enter a valid password"
            password = ""

        if not no_spaces(verify) or is_empty(verify) or not valid_len(verify):
            verify = "Reenter your password"
            verify = ""

        if password != verify:
            if not no_spaces(password) or is_empty(password) or not valid_len(password):
                password_error = "Enter a valid password"
                password = ""
            elif not no_spaces(verify) or is_empty(verify) or not valid_len(verify):
                verify_error = "Reenter your password"
                verify = ""
            else:
                password_error = "Passwords do not match"
                verify_error = "Passwords do not match"
                password = ""
                verify = ""
        
        if not username_error and not password_error and not verify_error:
            existing_user = User.query.filter_by(username=username).first()
            
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
            
            if existing_user:
                flash('User already exists')
                return render_template('signup.html')
            
            else:
                return render_template('signup.html',
                username=username,
                username_error=username_error,
                password_error=password_error,
                verify_error=verify_error)

    return render_template('signup.html')

def no_spaces(string):
    for char in string:
        if char == " ":
            return False
    return True

def is_empty(string):
    if string == " " or string == "":
        return True
    return False

def valid_len(string):
    if len(string) < 3 or len(string) > 20:
        return False
    return True

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blog():
    posts = Blog.query.all()

    if request.args:
        blog_id = request.args.get('id')
        blog_post = Blog.query.get(blog_id)

        return render_template('display_post.html', blog_post=blog_post)

    return render_template('blog.html', title="Build a Blog", posts=posts)
    
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username=session['username']).first()
    
    title_error = ""
    body_error = ""

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        
        if len(blog_title) == 0:
            title_error = 'Please fill in the title'
        
        if len(blog_body) == 0:
            body_error = 'Please fill in the body'
        
        if len(blog_title) == 0 and len(blog_body) == 0:
            title_error = 'Please fill in the title'
            body_error = 'Please fill in the body'
        
        if len(blog_title) != 0 and len(blog_body) != 0:
            blog_post = Blog(blog_title, blog_body, owner)
            db.session.add(blog_post)
            db.session.commit()
            flash('New post created!')
            id = blog_post.id
            return redirect('http://127.0.0.1:5000/blog?id={0}'.format(id))

        else:
            return render_template('newpost.html',
            blog_title=blog_title,
            blog_body=blog_body,
            title_error=title_error,
            body_error=body_error)

    return render_template('newpost.html', title="Add Blog Entry")

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

if __name__ == "__main__":
    app.run()