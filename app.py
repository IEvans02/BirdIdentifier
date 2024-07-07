import os
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from bird_classifier import classify_bird
import cv2
from keras.models import load_model
import numpy as np
from login import login_bp  # Import the login blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

# Register the login blueprint
app.register_blueprint(login_bp)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "mp4"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for the home page
@app.route("/")
def index():
    return render_template("index.html")


# Route for handling file upload and bird classification
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file part"

    file = request.files["file"]

    if file.filename == "":
        return "No selected file"

    if file and allowed_file(file.filename):
        # Check if the uploaded file is a video
        if file.filename.endswith(".mp4"):
            return process_video(file)

        # If not a video, assume it's an image
        return process_image(file)

    return "Invalid file format"


# Define the classes for bird breeds
bird_breeds = [
    "Blackbird",
    "Bluetit",
    "Carrion_Crow",
    "Chaffinch",
    "Coal_Tit",
    "Collared_Dove",
    "Dunnock",
    "Feral_Pigeon",
    "Goldfinch",
    "Great_Tit",
    "Greenfinch",
    "House_Sparrow",
    "Jackdaw",
    "Long_Tailed_Tit",
    "Magpie",
    "Robin",
    "Song_Thrush",
    "Starling",
    "Wood_Pigeon",
    "Wren",
]

model = load_model("model.h5")


def process_video(video_file):
    # Save the uploaded video file to the upload folder
    filename = secure_filename(video_file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
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


def process_image(image_file, confidence_threshold=0.4):
    # Save the uploaded image file to the upload folder
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image_file.save(filepath)

    # Load the image
    image = cv2.imread(filepath)

    # Resize the image to the expected input size (e.g., 150x150)
    input_size = (150, 150)
    image = cv2.resize(image, input_size)

    # Normalize pixel values
    image = image / 255.0

    # Run your bird classification model on the image
    predictions = model.predict(np.expand_dims(image, axis=0))
    predicted_class_indices = np.where(predictions[0] > confidence_threshold)[0]

    # Get the predicted bird class labels
    predicted_birds = [bird_breeds[i] for i in predicted_class_indices]

    if predicted_birds:
        # Combine predicted bird names
        text = ", ".join(predicted_birds)
        return text

    # If no birds were detected above the confidence threshold, return a message
    return "No birds detected above the confidence threshold"


if __name__ == "__main__":
    # Ensure the upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Handle form submission
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        # Here you could add logic to send an email, save the message to a database, etc.
        return render_template("contact.html", success=True)
    return render_template("contact.html")