from flask import Flask, request, send_file, render_template, url_for
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate_image():
    text = request.args.get('text', 'Hello')
    color = request.args.get('color', 'black')
    size = int(request.args.get('size', 40))

    valid_colors = ['black', 'red', 'blue', 'green', 'yellow', 'purple']
    if color not in valid_colors:
        return f"Invalid color. Choose from {', '.join(valid_colors)}.", 400

    if size < 10 or size > 100:
        return "Invalid size. Choose a size between 10 and 100.", 400

    image = Image.new('RGB', (len(text) * size, size), color='white')
    draw = ImageDraw.Draw(image)
    font_path = os.path.join(os.path.dirname(__file__), "arial.ttf")

    try:
        font = ImageFont.truetype(font_path, size)
    except IOError:
        return "Font file not found. Please ensure arial.ttf is in the same directory as app.py.", 500

    draw.text((10, 10), text, fill=color, font=font)
    image_path = os.path.join(os.path.dirname(__file__), 'static', 'label.png')
    image.save(image_path)

    return render_template('index.html', image_url=url_for('static', filename='label.png'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)

