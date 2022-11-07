from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash  
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from form import RegistrationForm, LoginForm, PostForm, MusicForm, RelationshipForm, SportForm, LifestyleForm, CommentForm
from flask_login import login_user, logout_user, login_required, LoginManager, UserMixin, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'my_login.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = '6b7631ea4878db'

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(70), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic = db.Column(db.String(), nullable=True)


    posts = db.relationship('Posts', backref='poster', lazy=True)
    posts = db.relationship('Music', backref='poster', lazy=True)
    posts = db.relationship('Relationship', backref='poster', lazy=True)
    posts = db.relationship('Sport', backref='poster', lazy=True)
    posts = db.relationship('Lifestyle', backref='poster', lazy=True)
    posts = db.relationship('Comment', backref='poster', lazy=True)
	  

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Create a Blog Post model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	author = db.Column(db.String(255))
	content = db.Column(db.Text)
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Create a Blog music model
class Music(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create a Blog relationship model
class Relationship(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create a Blog sport model
class Sport(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create a Blog lifestyle model
class Lifestyle(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Create a comment model
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foreign Key To Link Users (refer to primary key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))





@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = RegistrationForm()
	id = current_user.id
	name_to_update = User.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.username = request.form['username']
		name_to_update.email = request.form['email']
		
		
		# Check for profile pic
		if request.files['profile_pic']:
			name_to_update.profile_pic = request.files['profile_pic']

			# Grab Image Name
			pic_filename = secure_filename(name_to_update.profile_pic.filename)
			# Set UUID
			pic_name = str(uuid.uuid1()) + "_" + pic_filename
			# Save That Image
			saver = request.files['profile_pic']
			

			# Change it to a string to save to db
			name_to_update.profile_pic = pic_name
			try:
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
				flash("User Updated Successfully!")
				return render_template("dashboard.html", 
					form=form,
					name_to_update = name_to_update)
			except:
				flash("Error!  Looks like there was a problem...try again!")
				return render_template("dashboard.html", 
					form=form,
					name_to_update = name_to_update)
		else:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("dashboard.html", 
				form=form, 
				name_to_update = name_to_update)
	else:
		return render_template("dashboard.html", 
				form=form,
				name_to_update = name_to_update,
				id = id)


# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	# flash("You Have Been Logged Out!  Thanks For Stopping By...")
	return redirect(url_for('posts'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
				# Hash the password!!!
		hashed_pw = generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, first_name = form.firstname.data, last_name = form.lastname.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()

		flash('success')
		return redirect(url_for("login"))
	return render_template('signup.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
	log = LoginForm()
	if request.method=='POST':
		user = User.query.filter_by(username=log.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password, log.password.data):
				login_user(user)
				# flash("Login Succesfull!!")
				return redirect(url_for('index'))
			else: 
				# flash("Wrong Password - Try Again!")
				error =" Check your username and password and Try Again!"
				return render_template('login.html', error=error)
		else:
			flash('user does not exist')
	return render_template('login.html', log=log)

    

@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		poster = current_user.id
		post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, poster_id=poster, slug=form.slug.data)
		# Clear The Form
		form.title.data = ''
		form.author.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Add post data to database
		db.session.add(post)
		db.session.commit()
		# Return a Message
		flash("Blog Post Submitted Successfully!")
	# Redirect to the webpage 
	return render_template("add_post.html", form=form)


@app.route('/add-music', methods=['GET', 'POST'])
@login_required
def add_music():
	form = MusicForm()
	if form.validate_on_submit():
		poster = current_user.id
		post = Music(title=form.title.data, content=form.content.data, author=form.author.data, poster_id=poster, slug=form.slug.data)
		# Clear The Form
		form.title.data = ''
		form.author.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Add post data to database
		db.session.add(post)
		db.session.commit()
		# Return a Message
		flash("Blog Post Submitted Successfully!")
	# Redirect to the webpage 
	return render_template("add_post.html", form=form)

@app.route('/add-Relationship', methods=['GET', 'POST'])
@login_required
def add_Relationship():
	form = RelationshipForm()
	if form.validate_on_submit():
		poster = current_user.id
		post = Relationship(title=form.title.data, content=form.content.data, author=form.author.data, poster_id=poster, slug=form.slug.data)
		# Clear The Form
		form.title.data = ''
		form.author.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Add post data to database
		db.session.add(post)
		db.session.commit()
		# Return a Message
		flash("Blog Post Submitted Successfully!")
	# Redirect to the webpage 
	return render_template("add_post.html", form=form)

@app.route('/add-Sport', methods=['GET', 'POST'])
@login_required
def add_Sport():
	form = SportForm()
	if form.validate_on_submit():
		poster = current_user.id
		post = Sport(title=form.title.data, content=form.content.data, author=form.author.data, poster_id=poster, slug=form.slug.data)
		# Clear The Form
		form.title.data = ''
		form.author.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Add post data to database
		db.session.add(post)
		db.session.commit()
		# Return a Message
		flash("Blog Post Submitted Successfully!")
	# Redirect to the webpage 
	return render_template("add_post.html", form=form)

@app.route('/add-Lifestyle', methods=['GET', 'POST'])
@login_required
def add_Lifestyle():
	form = 	LifestyleForm()
	if form.validate_on_submit():
		poster = current_user.id
		post = Lifestyle(title=form.title.data, content=form.content.data, author=form.author.data, poster_id=poster, slug=form.slug.data)
		# Clear The Form
		form.title.data = ''
		form.author.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Add post data to database
		db.session.add(post)
		db.session.commit()
		# Return a Message
		flash("Blog Post Submitted Successfully!")
	# Redirect to the webpage 
	return render_template("add_post.html", form=form)

@app.route('/add-comment', methods=['GET', 'POST'])
@login_required
def add_comment():
	form = 	CommentForm()
	if form.validate_on_submit():
		poster = current_user.id
		com = Comment(content=form.content.data, slug=form.slug.data, author=form.author.data, poster_id=poster, title=form.title.data)
		# Clear The Form
		form.title.data = ''
		form.author.data = ''
		form.content.data = ''
		form.slug.data = ''
		# Add post data to database
		db.session.add(com)
		db.session.commit()
		# Return a Message
		flash("comment Submitted Successfully!")
	# Redirect to the webpage 
	return render_template("add_post.html", form=form)


@app.route('/posts')
def posts():
	# Grab all the posts from the database
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)

@app.route('/music')
def musics():
	# Grab all the posts from the database
	musics = Music.query.order_by(Music.date_posted)
	return render_template("music.html", musics=musics)

@app.route('/Relationships')
def Relationships():
	# Grab all the posts from the database
	Relationships = Relationship.query.order_by(Relationship.date_posted)
	return render_template("Relationship.html", Relationships=Relationships)

@app.route('/Sports')
def Sports():
	# Grab all the posts from the database
	Sports = Sport.query.order_by(Sport.date_posted)
	return render_template("player.html", Sports=Sports)

@app.route('/Lifestyles')
def Lifestyles():
	# Grab all the posts from the database
	Lifestyles = Lifestyle.query.order_by(Lifestyle.date_posted)
	return render_template("shoe.html", Lifestyles=Lifestyles)



@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)

@app.route('/dance/<int:id>')
def dance(id):
	dance = Music.query.get_or_404(id)
	return render_template('dance.html', dance=dance)

@app.route('/hands/<int:id>')
def hands(id):
	hands = Relationship.query.get_or_404(id)
	return render_template('hands.html', hands=hands)

@app.route('/ball/<int:id>')
def ball(id):
	ball = Sport.query.get_or_404(id)
	return render_template('ball.html', ball=ball)

@app.route('/cloth/<int:id>')
def cloth(id):
	cloth = Lifestyle.query.get_or_404(id)
	return render_template('cloth.html', cloth=cloth)

@app.route('/talk/<int:id>')
def talk(id):
	talk = Comment.query.get_or_404(id)
	return render_template('talk.html', talk=talk)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	news = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		news.title = form.title.data
 		#post.author = form.author.data
		news.slug = form.slug.data
		news.content = form.content.data
		# Update Database
		db.session.add(news)
		db.session.commit()
		flash("Post Has Been Updated!")
		return render_template('edit.html', form=form)
		
		
	
	if current_user.id == news.poster_id or current_user.id == 14:
		form.title.data = news.title
		# form.author.data = post.author
		form.slug.data = news.slug
		form.content.data = news.content
		return render_template('edit.html', form=form)
		
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Posts.query.order_by(Posts.date_posted)
		return render_template("posts.html", posts=posts)

@app.route('/music/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_music(id):
	post = Music.query.get_or_404(id)
	form = MusicForm()
	if form.validate_on_submit():
		post.title = form.title.data
 		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		# Update Database
		db.session.add(post)
		db.session.commit()
		flash("Post Has Been Updated!")
		return redirect(url_for('dance', id=post.id))
	
	if current_user.id == post.poster_id or current_user.id == 14:
		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Music.query.order_by(Music.date_posted)


@app.route('/Relationship/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_Relationship(id):
	post = Relationship.query.get_or_404(id)
	form = RelationshipForm()
	if form.validate_on_submit():
		post.title = form.title.data
 		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		# Update Database
		db.session.add(post)
		db.session.commit()
		flash("Post Has Been Updated!")
		return redirect(url_for('hands', id=post.id))
	
	if current_user.id == post.poster_id or current_user.id == 14:
		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Music.query.order_by(Music.date_posted)
		return render_template("Relationship.html", posts=posts)

@app.route('/Sport/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_Sport(id):
	post = Sport.query.get_or_404(id)
	form = SportForm()
	if form.validate_on_submit():
		post.title = form.title.data
 		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		# Update Database
		db.session.add(post)
		db.session.commit()
		flash("Post Has Been Updated!")
		return redirect(url_for('ball', id=post.id))
	
	if current_user.id == post.poster_id or current_user.id == 14:
		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Music.query.order_by(Music.date_posted)
		return render_template("player.html", posts=posts)

@app.route('/Lifestyle/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_Lifestyle(id):
	post = Lifestyle.query.get_or_404(id)
	form = LifestyleForm()
	if form.validate_on_submit():
		post.title = form.title.data
 		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		# Update Database
		db.session.add(post)
		db.session.commit()
		flash("Post Has Been Updated!")
		return redirect(url_for('cloth', id=post.id))
	
	if current_user.id == post.poster_id or current_user.id == 14:
		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Post...")
		posts = Music.query.order_by(Music.date_posted)
		return render_template("shoe.html", posts=posts)


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id) 
    try:
      db.session.delete(post_to_delete)
      db.session.commit()

			
      flash("Blog Post Was Deleted!")

			# Grab all the posts from the database so as to return to the blog page
      posts = Posts.query.order_by(Posts.date_posted)
      return redirect(url_for('posts'))

    except:
			# Return an error message
     flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
    posts = Posts.query.order_by(Posts.date_posted)
    return redirect(url_for('posts'))
    

@app.route('/music/delete/<int:id>')
@login_required
def delete_music(id):
    post_to_delete = Music.query.get_or_404(id) 
    try:
      db.session.delete(post_to_delete)
      db.session.commit()

			# Return a message
      flash("Blog Post Was Deleted!")

			# Grab all the posts from the database so as to return to the blog page
      posts = Music.query.order_by(Music.date_posted)
      return redirect(url_for('musics'))


    except:
			# Return an error message
     flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
    posts = Music.query.order_by(Music.date_posted)
    return redirect(url_for('musics'))

@app.route('/Relationship/delete/<int:id>')
@login_required
def delete_Relationship(id):
    post_to_delete = Relationship.query.get_or_404(id) 
    try:
      db.session.delete(post_to_delete)
      db.session.commit()

			# Return a message
      flash("Blog Post Was Deleted!")

			# Grab all the posts from the database so as to return to the blog page
      posts = Relationship.query.order_by(Relationship.date_posted)
      return redirect(url_for('Relationships'))



    except:
			# Return an error message
     flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
    posts = Relationship.query.order_by(Relationship.date_posted)
    return redirect(url_for('Relationships'))


@app.route('/Sport/delete/<int:id>')
@login_required
def delete_Sport(id):
    post_to_delete = Sport.query.get_or_404(id) 
    try:
      db.session.delete(post_to_delete)
      db.session.commit()

			# Return a message
      flash("Blog Post Was Deleted!")

			# Grab all the posts from the database so as to return to the blog page
      posts = Sport.query.order_by(Sport.date_posted)
      return redirect(url_for('Sports'))



    except:
			# Return an error message
     flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
    posts = Relationship.query.order_by(Relationship.date_posted)
    return redirect(url_for('Sports'))
    


@app.route('/Lifestyle/delete/<int:id>')
@login_required
def delete_Lifestyle(id):
    post_to_delete = Lifestyle.query.get_or_404(id) 
    try:
      db.session.delete(post_to_delete)
      db.session.commit()

			# Return a message
      flash("Blog Post Was Deleted!")

			# Grab all the posts from the database so as to return to the blog page
      posts = Lifestyle.query.order_by(Lifestyle.date_posted)
      return redirect(url_for('Lifestyles'))


    except:
			# Return an error message
     flash("Whoops! There was a problem deleting post, try again...")

			# Grab all the posts from the database
    posts = Lifestyle.query.order_by(Lifestyle.date_posted)
    return redirect(url_for('Lifestyles'))
  


@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = RegistrationForm()
	name_to_update = User.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.username = request.form['username']
		name_to_update.email = request.form['email']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
		except:
			flash("Error!  Looks like there was a problem...try again!")
			return render_template("update.html", form=form, name_to_update=name_to_update, id=id)
	else:
		return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
        


@app.route('/about')
def about():
    return render_template('about.html')	


if __name__ == '__main__':
    app.run(debug=True)