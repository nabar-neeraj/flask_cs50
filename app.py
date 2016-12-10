from flask import Flask, render_template, request, redirect, url_for
from models import *

app = Flask(__name__)

@app.before_request
def before_request():
	# Create db if needed and connect
	initialize_db()

# Only after successful request
# @app.after_request

# After any request (success/fail)
@app.teardown_request
def teardown_request(exception):
	db.close()

@app.route('/')
def home():
	return render_template('home.html',posts=Post.select().order_by(Post.date_posted.desc()))

@app.route('/new_post')
def new_post():
	return render_template('new_post.html')

@app.route('/create',methods=['POST'])
def create_post():
	print request.form
	# Create the post
	Post.create(
			title = request.form['title'],
			text = request.form['text']
		)

	# Redirect the user to the homepage
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)