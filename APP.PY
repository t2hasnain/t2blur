from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
import os

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'  # Use the /tmp directory for serverless functions
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''<html>
        <body>
            <h1>Upload an Image</h1>
            <input type="file" id="fileInput" accept="image/*">
            <button id="uploadButton">Upload</button>
            <div id="imageContainer" style="display:none;">
                <h2>Blurred Image</h2>
                <img id="blurredImage" src="" alt="Blurred Image">
                <a id="downloadLink" href="#" download>Download Blurred Image</a>
            </div>
            <script>
                document.getElementById('uploadButton').addEventListener('click', async () => {
                    const fileInput = document.getElementById('fileInput');
                    if (fileInput.files.length === 0) {
                        alert('Please select a file!');
                        return;
                    }
                    const formData = new FormData();
                    formData.append('file', fileInput.files[0]);
                    const response = await fetch('/upload', {
                        method: 'POST',
                        body: formData,
                    });
                    if (response.ok) {
                        const imagePath = await response.text();
                        const blurredImage = document.getElementById('blurredImage');
                        blurredImage.src = imagePath;
                        document.getElementById('imageContainer').style.display = 'block';
                        const downloadLink = document.getElementById('downloadLink');
                        downloadLink.href = imagePath;
                    } else {
                        alert('Error uploading image!');
                    }
                });
            </script>
        </body>
    </html>'''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Blur the image
    image = Image.open(file_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(10))
    blurred_image_path = os.path.join(UPLOAD_FOLDER, 'blurred_' + file.filename)
    blurred_image.save(blurred_image_path)

    return blurred_image_path

if __name__ == '__main__':
    app.run()
