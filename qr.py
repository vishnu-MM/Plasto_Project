from flask import Flask, render_template, request
from pyzbar import decode

app = Flask(__name__)

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        # Get the uploaded image file
        image = request.files['image']
        # Decode the QR code from the image
        decoded_data = decode(image)
        # Get the decoded data from the QR code
        qr_data = decoded_data[0].data.decode()
        # Do something with the QR code data
        # ...
    return render_template('scan.html')