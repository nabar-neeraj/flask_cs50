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

@app.route('/delete_post/<post_id>', methods=['GET'])
def delete_post(post_id):
	print "Selected post",Post.get(id=post_id)
	post_to_delete = Post.get(id=post_id)
	# print "Removing",post_to_delete['title']
	post_to_delete.delete_instance()
	return redirect(url_for('home'))

@app.route('/edit_post/<post_id>', methods=['GET','POST'])
def edit_post(post_id):
	print "Selected post",Post.get(id=post_id)
	post_to_update = Post.get(id=post_id)
	if request.method == 'GET':
		return render_template('edit.html',post_info = post_to_update)
	if request.method == 'POST':
		print request.form['title']
		print request.form['text']
		post_to_update.title = request.form['title']
		post_to_update.text = request.form['text']
		post_to_update.save()
		return redirect(url_for('home'))
	

if __name__ == '__main__':
	app.run(debug=True)