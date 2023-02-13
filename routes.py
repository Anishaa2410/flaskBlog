from fileinput import filename
from flask import *  
import os, secrets
from flaskblog.form import RegisterationForm,LoginForm, AccountUpdateForm ,PostForm
from flaskblog import app,db,bcr
from flaskblog.model import User, Post
from flask_login import login_user, current_user, logout_user,login_required

# posts=[
#     {
#         'author' : 'Anisha',
#         'date' : '3rd Oct',
#         'title' : 'blog1',
#         'content' : 'java',
#     },

#     {
#         'author' : 'Ani',
#         'date' : '30th Jan',
#         'title' : 'blog2',
#         'content' : 'javac',
#     }
# ]
abouts=[
    {
    'name1' : 'Anisha',
    'name2' : 'xyz',
    'name3' : 'abc',
    'name4' : 'mnb',
    'num1' : '9520556933',
    'num2' : '908753732',
    'num3' : '098223456',
    'num4' : '908633456',
    }
    
]


 
@app.route('/')  
def home():  
    posts = Post.query.all()
    return render_template("home.html", posts=posts, title="home")  
 
@app.route('/about')  
def about():  
    return render_template("about.html", abouts=abouts, title='AboutUs')

@app.route('/register', methods=['POST','GET'])  
def register():  
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # creating instance of form
    form= RegisterationForm()  
    if form.validate_on_submit():
        phash = bcr.generate_password_hash(form.password.data).decode('utf-8')
        user= User(username= form.username.data , email= form.email.data , password = phash )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for { form.username.data }!! Now you can login", "success")
        return redirect(url_for('login'))
    return render_template("register.html",  title='Register', form=form)

@app.route('/login', methods=['POST','GET'])  
def login():  
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()  
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcr.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page= request.args.get('next')
            # using ternary operator, if there are some arguements in url,they will get stored in next_page and after login,that page will be redirected
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Check username and password!' , 'danger')
    return render_template("login.html",  title='Login', form=form)


@app.route('/logout', methods=['POST','GET'])  
def logout():  
    logout_user()
    return redirect(url_for('home'))


def save_pic(pic): #this function is used so that every image uploaded has different name
    random_hex = secrets.token_hex(6)
    _ , f_ext = os.path.splitext(pic.filename) # underscore can be used to name variables that arent used
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path,'static/profilePic', pic_fn)
    pic.save(pic_path)
    return pic_fn

@app.route('/account', methods=['POST','GET'])
@login_required  
def account():  
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_pic(form.picture.data)
            current_user.image_file = pic_file
        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash("Updated", "success")
        return redirect(url_for("account"))
    if request.method=='GET':      #to make sure that fields have value of current user already istead of blank space
        form.username.data= current_user.username
        form.email.data= current_user.email

    image= url_for('static', filename= 'profilePic/' + current_user.image_file)
    return render_template("account.html",  title='Account' , image_file= image, form = form)

@app.route('/post/new', methods=['POST','GET'])
@login_required  
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post =Post(title=form.title.data , content = form.content.data , author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Created!!' , 'success')
        return redirect(url_for('home'))
    return render_template("post.html",  title='New Post', form = form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post1.html",  title=post.title, post= post)

