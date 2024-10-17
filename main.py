import os
from flask import Flask, request, jsonify

import google.auth
import vertexai
from vertexai.generative_models import GenerativeModel

_, project = google.auth.default()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def validate_kyc_document():
    # Specify the file path directly
    file_path = "/home/nikita_datascience/passport-front.jpg"

    # Initialize Vertex AI with the project and location
    vertexai.init(project=project, location="us-central1")

    # Create a GenerativeModel instance
    model = GenerativeModel("gemini-1.5-flash")

    # Build the prompt using the file path
    prompt = f"Process the KYC document at '{file_path}' and verify the validity of its content, focusing on expiry dates and personal information accuracy. Please return the results in JSON format."
    
    # Generate response from the model
    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))