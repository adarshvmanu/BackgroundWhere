# app.py
import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from rembg import remove

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'

# Background removal function using rembg
def remove_background(image_path):
    # Load the image
    with open(image_path, "rb") as f:
        image_data = f.read()

    # Perform background removal using rembg
    result = remove(image_data)

    # Save the processed image
    processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], os.path.basename(image_path))
    with open(processed_image_path, "wb") as f:
        f.write(result)

    return processed_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file selected."}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
    image_file.save(image_path)

    processed_image_path = remove_background(image_path)
    processed_filename = os.path.basename(processed_image_path)

    return jsonify({"processed_image": processed_filename})

@app.route('/processed/<filename>')
def processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)
