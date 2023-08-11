import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from bird_classifier import classify_bird

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file upload and bird classification
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        # Save the uploaded file to a temporary location
        filename = secure_filename(file.filename)
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_filepath)

        # Process the image using the bird classification model
        predicted_bird = classify_bird(temp_filepath)

        # Remove the temporary file
        os.remove(temp_filepath)

        return f"Predicted Bird: {predicted_bird}"

if __name__ == '__main__':
    # Configure the upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.run(debug=True)

