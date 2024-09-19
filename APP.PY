from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageFilter
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Uploader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #f0f0f0;
            margin: 0;
        }
        .container {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        input[type="file"] {
            margin-bottom: 20px;
        }
        .hidden {
            display: none;
        }
        img {
            max-width: 100%;
            height: auto;
            margin-top: 20px;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload an Image</h1>
        <input type="file" id="fileInput" accept="image/*">
        <button id="uploadButton">Upload</button>
        <div id="imageContainer" class="hidden">
            <h2>Blurred Image</h2>
            <img id="blurredImage" src="" alt="Blurred Image">
            <a id="downloadLink" href="#" class="hidden" download>Download Blurred Image</a>
        </div>
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
                document.getElementById('imageContainer').classList.remove('hidden');
                
                const downloadLink = document.getElementById('downloadLink');
                downloadLink.href = imagePath;
                downloadLink.classList.remove('hidden');
            } else {
                alert('Error uploading image!');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
    app.run(debug=True)
