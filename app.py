from flask import Flask, render_template, request, redirect, url_for, flash
import json

from form import RegistrationForm, LoginForm

app = Flask(__name__)



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    post_index = next((i for (i, post) in enumerate(blog_posts) if post['id'] == post_id), None)
    if post_index is None:
        return "Post not found", 404
    post = blog_posts[post_index]

    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)
        return redirect(url_for('home'))

    return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

        post_index = next((i for (i, post) in enumerate(blog_posts) if post['id'] == post_id), None)
        if post_index is None:
            return "Post not found", 404
        del blog_posts[post_index]

    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content}

        blog_posts.append(new_post)
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        return redirect(url_for('home'))
    return render_template('add.html', title="Add Post")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


@app.route('/')
@app.route('/home')
def home():
    with open('blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(debug=True)
