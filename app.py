import openai
import os
import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')



resume_text = extract_text_from_pdf("resume/resume.pdf")

job_description = """
Junior Software Developer
Requirements:
- Python or JavaScript
- Basic SQL
- Git/GitHub
- Problem-solving skills
"""

with open("prompts/v1_generic.txt", "r") as f:
    prompt_template = f.read()

prompt = prompt_template.replace("{{RESUME_TEXT}}", resume_text)\
                        .replace("{{JOB_DESCRIPTION}}", job_description)

response = openai.ChatCompletion.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2
)

print(response.choices[0].message.content)
