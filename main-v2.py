import os
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image

import google.auth
import vertexai
from vertexai.generative_models import GenerativeModel

_, project = google.auth.default()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def validate_kyc_document():
    # Path to your KYC document image
    file_path = "/home/nikita_datascience/kyc-verification-llms/passport-front.jpg"
    
    # Using Pytesseract to convert image to text
    try:
        extracted_text = pytesseract.image_to_string(Image.open(file_path))
    except Exception as e:
        return jsonify({"error": str(e)})

    # Initialize Vertex AI with the project and location
    vertexai.init(project=project, location="us-central1")

    # Create a GenerativeModel instance
    model = GenerativeModel("gemini-1.5-flash")

    # Build the prompt using the extracted text
    prompt = f"Verify the following KYC data for its validity, focusing on expiry dates and personal information accuracy: \n{extracted_text}\nPlease return the results in JSON format."
    
    # Generate response from the model
    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))