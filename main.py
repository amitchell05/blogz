from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:holi!f4me@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'wTq2aV3ssbqsvaSW'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(250))

    def __init__(self, title, body):
        self.title = title
        self.body = body

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
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()
            session
            id = new_post.id
            flash('New post created!')
            return render_template('display_post.html', id=id)

        else:
            return render_template('newpost.html',
            blog_title=blog_title,
            blog_body=blog_body,
            title_error=title_error,
            body_error=body_error)

    return render_template('newpost.html', title="Add Blog Entry")


if __name__ == "__main__":
    app.run()
