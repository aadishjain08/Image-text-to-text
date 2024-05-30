import base64
import easyocr
from flask import Flask, request, jsonify, render_template
import io
from PIL import Image
import os
app = Flask(__name__)


import re

def clean_text(text):
    # Remove non-alphanumeric characters and extra whitespace
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text

def read_text_from_image(image_data):
    try:
        # Open the image from the uploaded file
        image = Image.open(image_data)

        # Create an OCR reader object
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image)

        # Extract text from the result
        text = ' '.join([entry[1] for entry in result])

        cleaned_text = clean_text(text)

        return cleaned_text

        # return text
    except Exception as e:
        print("Error:", e)
        return None


@app.route('/')
def start():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify(message='No image provided'), 400
        
        image = request.files['image']
        if image.filename == '':
            return jsonify(message='No selected file'), 400
        image_data=image.read()
        text = read_text_from_image(image)
        if text:
            base64_image = base64.b64encode(image_data).decode('utf-8')
            return render_template('output.html', base64_image=base64_image,name=text), 200
        else:
            return jsonify(message='Text not found'), 404
    except Exception as e:
        return jsonify(message=str(e), error='error'), 500


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'production'
    app.run(debug=True)
