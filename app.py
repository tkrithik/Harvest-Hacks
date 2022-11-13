# -----------Import Commands-----------
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, os.path
from vision import Vision

vision = Vision()

# Flask config
app = Flask(__name__)

fruit_title, fruit_url, fruit_content, fruit_image = None, None, None, None

@app.route("/", methods=["GET", "POST"])
def index():
    ''' This function lets you create a local flask page, which we have assigned to /,
    thus meaning the route is simply the local host, without any subdomain to navigate to.
    The index function starts by getting the file the user uploaded, and then creates a new copy of the file locally.
    Then, using other functions, it converts from sound to text, then to sound again and pushes back to the user.'''
    if request.method == "POST":
        file_object = request.files["file"]
        file_path = os.path.join('resources/',
                                 secure_filename(file_object.filename))
        file_object.save(file_path)

        global fruit_title, fruit_url, fruit_content, fruit_image
        fruit_title, fruit_url, fruit_content, fruit_image = vision.process_image(file_path)

        return render_template('button.html')
    return render_template('index.html')  # Html template

@app.route('/fruits/')
def fruits_page():
    return render_template('test.html', title = fruit_title, url = fruit_url, content = fruit_content, image = fruit_image)