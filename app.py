import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from bird_classifier import classify_bird
import cv2

app = Flask(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

    if file and allowed_file(file.filename):
        # Check if the uploaded file is a video
        if file.filename.endswith('.mp4'):
            return process_video(file)

        # If not a video, assume it's an image
        return process_image(file)

    return "Invalid file format"

def process_video(video_file):
    # Save the uploaded video file to the upload folder
    filename = secure_filename(video_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_file.save(filepath)

    # Initialize video capture
    cap = cv2.VideoCapture(filepath)

    if not cap.isOpened():
        return "Error opening video file."

    # Initialize results list to store birds found in the video
    video_results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Classify the current frame
        predicted_bird = classify_bird(frame)
        video_results.append(predicted_bird)

    # Release video capture and remove the uploaded file
    cap.release()
    os.remove(filepath)

    # Return the list of birds found in the video as JSON
    return jsonify(video_results)

def process_image(image_file):
    # Save the uploaded image file to the upload folder
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(filepath)

    # Load the image and classify the bird breed
    image = cv2.imread(filepath)
    predicted_bird = classify_bird(image)

    # Remove the uploaded file
    os.remove(filepath)

    return f"Predicted Bird Breed: {predicted_bird}"

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
