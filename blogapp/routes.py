import os
import secrets
from PIL import Image
from flask import render_template , url_for , flash , redirect, request, abort
from blogapp import app, db , bcrypt, mail
from blogapp.forms import Registration , Login , UpdateAccountForm , PostForm , RequestResetForm , ResetPasswordForm, AddCommentForm
from blogapp.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message



@app.route('/')
@app.route('/home')
def home():
    return  render_template('main.html' , title = 'WeShare')

@app.route('/all')
def all():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('home.html' , posts = posts)

@app.route('/about')
def about():
    return  render_template('about.html' , title = 'about')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return  render_template('register.html' , title = 'Register', form = form)
    




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please Check Your Informations ', 'error') #error is the flash message comment

    return  render_template('login.html' , title = 'login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profil_pics', picture_fn)

    output_size = (150, 150)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account' , methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account had been updated' , 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profil_pics/' + current_user.image_file)
    return  render_template('account.html' , title = 'account' , image_file= image_file , form = form)

    
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('all'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')


#----------------------------------- Categories--------------------------------------------
@app.route('/academic')
def academic():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='Academic').order_by(Post.date_posted.desc()).paginate(page=page, per_page=7) 
    return  render_template('categories/academic.html' , posts = posts , category = 'academic')


@app.route('/post/academic', methods=['GET', 'POST'])
@login_required
def academicpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('academic'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')



@app.route('/technology')
def technology():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='technology').order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('categories/technology.html' , posts = posts)


@app.route('/post/technology', methods=['GET', 'POST'])
@login_required
def technologypost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('technology'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')


@app.route('/sport')
def sport():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='sport').order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('categories/sport.html' , posts = posts)


@app.route('/post/sport', methods=['GET', 'POST'])
@login_required
def sportpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('sport'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')



@app.route('/travel')
def travel():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='travel').order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('categories/travel.html' , posts = posts)


@app.route('/post/travel', methods=['GET', 'POST'])
@login_required
def travelpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('travel'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')


@app.route('/gaming')
def gaming():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='gaming').order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('categories/gaming.html' , posts = posts)


@app.route('/post/gaming', methods=['GET', 'POST'])
@login_required
def gamingpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('gaming'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')


@app.route('/animals')
def animals():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category='animals').order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('categories/animals.html' , posts = posts)


@app.route('/post/animals', methods=['GET', 'POST'])
@login_required
def animalspost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data , author = current_user,
                    category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success' )
        return redirect(url_for('animals'))
    return  render_template('create_post.html' , title = 'New Post' , form = form, legend = 'New Post')


#-----------------------------------------------------------------------------------------------------------


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post_id=post.id, owner = current_user)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(url_for("post", post_id=post.id))
    return render_template('post.html', title=post.title , post=post, form=form)



@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        db.session.commit()
        flash('Your Post has been updated' , 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': 
        form.title.data = post.title 
        form.content.data = post.content 
    return  render_template('create_post.html' , title = 'Update Post' , form = form , legend = 'Update Post' )

@app.route('/post/<int:post_id>/delete', methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted ! ', 'success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=7)
    return  render_template('user_posts.html' , posts = posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request' , sender='noreply@weshare.com' , recipients=[user.email])
    msg.body = f""" To reset your password , visit the following link:
{url_for('reset_token' , token = token , _external=True)}
    
this link expires in 30 minutes 
"""
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with intructions to reset your password.' , 'success')
        return redirect(url_for('login'))
    return  render_template('reset_request.html' , title ='Reset Password', form = form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an expired token' , 'warning')
        return redirect(url_for('reset_requests'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your Password has been updated , you are now able to login', 'success')
        return redirect(url_for('login'))
    
    return  render_template('reset_token.html' , title ='Reset Password', form = form)

