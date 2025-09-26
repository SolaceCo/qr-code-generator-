from flask import Flask, request, make_response, render_template_string
import qrcode
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Custom QR Code Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        form { margin-bottom: 20px; }
        input[type="text"] { width: 100%; }
        .ads { margin-top: 20px; text-align: center; }
    </style>
</head>
<body>
    <h1>Custom QR Code Generator</h1>
    <p>Enter text or URL to generate a QR code.</p>
    <form method="post">
        <input type="text" name="data" placeholder="Enter text or URL..." required><br>
        <label>Fill Color: <input type="color" name="fill_color" value="#000000"></label><br>
        <label>Back Color: <input type="color" name="back_color" value="#FFFFFF"></label><br>
        <button type="submit">Generate QR Code</button>
    </form>
    <div class="ads">
        <!-- Example AdSense placeholder; replace with your code later -->
        <p>Ads will go here.</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form['data']
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#FFFFFF')
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image with custom colors
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Save to buffer
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = buffered.getvalue()
        
        # Return as downloadable image
        response = make_response(img_str)
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = 'attachment; filename=qr_code.png'
        return response
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
