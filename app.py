from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os
import random
import string

app = Flask(__name__)
app.config['JSON_PATH'] = 'blogs.json'

# Ensure the JSON file exists and initialize with an empty list if it doesn't
if not os.path.exists(app.config['JSON_PATH']):
    with open(app.config['JSON_PATH'], 'w') as f:
        json.dump([], f)

# Helper function to load JSON data
def load_data():
    with open(app.config['JSON_PATH'], 'r') as json_file:
        data = json.load(json_file)
    return data

# Helper function to save JSON data
def save_data(data):
    with open(app.config['JSON_PATH'], 'w') as json_file:
        json.dump(data, json_file, indent=4)

@app.route('/')
def index():
    blogs = load_data()
    return render_template('index.html', blogs=blogs)

@app.route('/write', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        username = request.form['username']
        blog_text = request.form['blog_text']
        publish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_blog = {
            'id': ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            'username': username,
            'blog_text': blog_text,
            'edit_count': 0,
            'publish_time': publish_time
        }
        blogs = load_data()
        blogs.append(new_blog)
        save_data(blogs)
        return redirect(url_for('index'))
    return render_template('write.html')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_blog(id):
    blogs = load_data()
    blog_to_update = next((blog for blog in blogs if blog['id'] == id), None)
    if request.method == 'POST':
        if blog_to_update:
            blog_to_update['blog_text'] = request.form['blog_text']
            blog_to_update['edit_count'] += 1
            save_data(blogs)
        return redirect(url_for('index'))
    return render_template('update.html', blog=blog_to_update)

@app.route('/delete/<id>', methods=['POST'])
def delete_blog(id):
    blogs = load_data()
    blogs = [blog for blog in blogs if blog['id'] != id]
    save_data(blogs)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
