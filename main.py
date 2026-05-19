from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
import re
import os

app = FastAPI()

UPLOAD_FOLDER = "resumes"

# Create folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_text_from_pdf(pdf_path):
    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        text += page.extract_text()

    return text

# -----------------------------
# Extract email
# -----------------------------
def extract_email(text):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    match = re.search(email_pattern, text)

    return match.group(0) if match else None

# -----------------------------
# Extract phone number
# -----------------------------
def extract_phone(text):
    phone_pattern = r"\+?\d[\d -]{8,12}\d"

    match = re.search(phone_pattern, text)

    return match.group(0) if match else None

# -----------------------------
# Extract skills
# -----------------------------
def extract_skills(text):
    skills_list = [
        "Python",
        "Java",
        "C++",
        "SQL",
        "Machine Learning",
        "FastAPI",
        "Django",
        "Flask",
        "JavaScript"
    ]

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills

# -----------------------------
# API Route
# -----------------------------
@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    text = extract_text_from_pdf(file_path)

    # Extract info
    email = extract_email(text)
    phone = extract_phone(text)
    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "email": email,
        "phone": phone,
        "skills": skills
    }