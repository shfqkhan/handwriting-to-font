from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import base64

app = Flask(_name_)

# Route to test if the app is working
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Handwriting to Font API is running!"})

# Route to process handwriting and return text
@app.route("/recognize", methods=["POST"])
def recognize_handwriting():
    try:
        # Get the image from request
        data = request.json.get("image")
        if not data:
            return jsonify({"error": "No image data provided"}), 400

        # Decode base64 image
        image_bytes = base64.b64decode(data)
        image = Image.open(io.BytesIO(image_bytes))

        # Use Tesseract OCR to extract text
        extracted_text = pytesseract.image_to_string(image)

        return jsonify({
            "status": "success",
            "extracted_text": extracted_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if _name_ == "_main_":
    app.run(debug=True)
