from gc import get_objects
import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flask_blog import app, db, bcrypt, mail
from flask_blog.models import User, Post
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm,ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask.views import View


@app.route("/",methods=['GET','POST'])
@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next') # To redirect to the requested page after login... 
            return redirect(next_page) if next_page else redirect(url_for('homePage'))
        else:
            flash(f'Logging In Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route("/home")
@login_required
def homePage():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('index.html', posts=posts, title='title')


@app.route("/about")
@login_required
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Accounted created successfully. You can log In', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fname = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pic',picture_fname)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fname

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.username.data == current_user.username and not form.picture.data:
            pass
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your Account has been updated successfully','success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file, form=form, user=current_user)

@app.route('/account/<int:user_id>/delete',methods=['POST'])
@login_required
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        abort(403)
    User.query.filter_by(username=user.username).delete()
    Post.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    flash('Your Account has been deleted','success')
    return redirect(url_for('logout'))


@app.route('/new/post', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        blog = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('homePage'))
    return render_template('create_post.html',title='New Post',form=form, legend='New Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been Updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted','success')
    return redirect(url_for('homePage'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
            .paginate(page=page,per_page=5)
    return render_template('user_posts.html',user=user, posts=posts, title='title')

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To Reset the password, Click the following Link:
{url_for('reset_token',token=token,_external=True)}

If you did not make this request, then simply ignore the mail and no changes will be done'''
    mail.send(msg)

@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password',form=form)


@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f'Password successfully changed. You can log In Now', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',title='Request Password',form=form)


