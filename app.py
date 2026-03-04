import os
from flask import Flask, render_template, request
from resume_checker import analyze_resume

import pdfplumber
import pytesseract
from PIL import Image
import io

app = Flask(__name__)


# -------- PDF TEXT EXTRACTION --------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


# -------- IMAGE OCR EXTRACTION --------
def extract_text_from_image(file):

    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes))

    text = pytesseract.image_to_string(image)

    return text


# -------- MAIN ROUTE --------
@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    if request.method == "POST":

        job_desc = request.form.get("job_desc", "")
        resume_text = ""

        # -------- CHECK FILE UPLOAD --------
        if "resume_file" in request.files:

            file = request.files["resume_file"]

            if file.filename != "":

                filename = file.filename.lower()

                # PDF
                if filename.endswith(".pdf"):
                    resume_text = extract_text_from_pdf(file)

                # Image
                elif filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    resume_text = extract_text_from_image(file)

        # -------- FALLBACK: TEXTAREA --------
        if resume_text == "":
            resume_text = request.form.get("resume", "")

        # -------- ANALYZE RESUME --------
        result = analyze_resume(resume_text, job_desc)

    return render_template("index.html", result=result)


# -------- RUN SERVER --------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)