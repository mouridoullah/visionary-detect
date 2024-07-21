from flask import Flask, request, jsonify
import requests
from io import BytesIO
from PIL import Image
from detector import detect_objects

app = Flask(__name__)

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise ValueError(f"Unable to download image from URL. Status code: {response.status_code}")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    image_url = data.get('image_url')
    img = download_image(image_url)
    img.save('/tmp/temp_image.jpg')
    detection_result = detect_objects('/tmp/temp_image.jpg')
    return jsonify({'prediction': detection_result.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
