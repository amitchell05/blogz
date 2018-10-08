from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True

posts = []

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        posts.append((title, body))
    
    return render_template('newpost.html', title="Add a Blog Entry", posts=posts)

app.run()

"""app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:holi!f4me@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)"""

"""class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    return render_template('blog.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if len(title) != 0 and len(body) != 0:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            flash('New post created')
            return redirect('/blog', new_post=new_post)
        else:
            flash('Blog title or blog content invalid')

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
"""