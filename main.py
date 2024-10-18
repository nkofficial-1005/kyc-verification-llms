# import os
# from flask import Flask, request, jsonify

# import google.auth
# import vertexai
# from vertexai.generative_models import GenerativeModel

# _, project = google.auth.default()

# app = Flask(__name__)

# @app.route("/", methods=['GET', 'POST'])
# def validate_kyc_document():
#     # Specify the file path directly
#     file_path = "/home/nikita_datascience/passport-front.jpg"

#     # Initialize Vertex AI with the project and location
#     vertexai.init(project=project, location="us-central1")

#     # Create a GenerativeModel instance
#     model = GenerativeModel("gemini-1.5-flash")

#     # Build the prompt using the file path
#     prompt = f"Process the KYC document at '{file_path}' and verify the validity of its content, focusing on expiry dates and personal information accuracy. Please return the results in JSON format."
    
#     # Generate response from the model
#     response = model.generate_content(prompt)
#     return jsonify({"response": response.text})

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# import os
# from flask import Flask, request, jsonify

# import google.auth
# import vertexai
# from vertexai.generative_models import GenerativeModel

# _, project = google.auth.default()

# app = Flask(__name__)

# @app.route("/", methods=['GET', 'POST'])
# def validate_kyc_document():
#     # Simulated extracted content from the document
#     document_content = """
#     Name: John Doe
#     Date of Birth: 1990-01-01
#     Document Number: AB1234567
#     Expiry Date: 2025-12-31
#     Issuing Country: USA
#     """

#     # Initialize Vertex AI with the project and location
#     vertexai.init(project=project, location="us-central1")

#     # Create a GenerativeModel instance
#     model = GenerativeModel("gemini-1.5-flash")

#     # Build the prompt using the extracted text
#     prompt = f"Verify the following KYC data for its validity, focusing on expiry dates and personal information accuracy: {document_content} Please return the results in JSON format."
    
#     # Generate response from the model
#     response = model.generate_content(prompt)
#     return jsonify({"response": response.text})

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

import os
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image

import google.auth
import vertexai
from vertexai.generative_models import GenerativeModel

_, project = google.auth.default()

pytesseract.pytesseract.tesseract_cmd = '~/.local/bin/tesseract'

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def validate_kyc_document():
    # Path to your KYC document image
    file_path = "passport-front.jpg"
    
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