import re
import PyPDF2
import requests
import io
import nltk
from nltk.tokenize import word_tokenize

# Download the punkt tokenizer
nltk.download('punkt')

def extract_text_from_pdf(file_path_or_url):
    text = ""
    
    if file_path_or_url.startswith('http'):
        response = requests.get(file_path_or_url)
        if response.status_code == 200:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
        else:
            print(f"Failed to download PDF from {file_path_or_url}")
            return text
    else:
        with open(file_path_or_url, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
        
    return text

def analyze_freelancer(text):
    skills = set()
    blockchain_languages_known = []
    job_title = ""
    total_experience_years = 0
    rating = 0
    reasons = []
    rejection_reasons = []
    
    frontend_languages = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue']
    backend_languages = ['Python', 'Ruby', 'PHP', 'Node.js', 'Java', 'C#', 'Go']
    blockchain_languages = ['Solidity', 'Rust', 'C++', 'Vyper', 'Huff', 'Go (Golang)']
    soft_skills = ['teamwork', 'communication', 'problem-solving', 'leadership', 'creativity']

    # Soft skills detection using NLP
    tokenized_text = word_tokenize(text.lower())
    for skill in soft_skills:
        if skill in tokenized_text:
            reasons.append(f"Has soft skill: {skill}")
            rating += 0.5
        else:
            rejection_reasons.append(f"Lacks soft skill: {skill}")

    # Technical skills
    for lang in frontend_languages:
        if re.search(rf'\b{lang}\b', text, re.IGNORECASE):
            skills.add(lang)
            reasons.append(f"Knows frontend language: {lang}")
            rating += 0.5
        else:
            rejection_reasons.append(f"Lacks frontend language: {lang}")

    for lang in backend_languages:
        if re.search(rf'\b{lang}\b', text, re.IGNORECASE):
            skills.add(lang)
            reasons.append(f"Knows backend language: {lang}")
            rating += 1
        else:
            rejection_reasons.append(f"Lacks backend language: {lang}")

    for lang in blockchain_languages:
        if re.search(rf'\b{lang}\b', text, re.IGNORECASE):
            blockchain_languages_known.append(lang)
            skills.add(lang)
            reasons.append(f"Knows blockchain language: {lang}")
            rating += 1.5
        else:
            rejection_reasons.append(f"Lacks blockchain language: {lang}")

    # Job title and experience
    if skills:
        if skills.intersection(frontend_languages) and skills.intersection(backend_languages):
            job_title = "Fullstack Developer"
            reasons.append("Is a Fullstack Developer")
            rating += 2
        elif skills.intersection(frontend_languages):
            job_title = "Frontend Developer"
            reasons.append("Is a Frontend Developer")
            rating += 1
        elif skills.intersection(backend_languages):
            job_title = "Backend Developer"
            reasons.append("Is a Backend Developer")
            rating += 1
    else:
        rejection_reasons.append("Lacks sufficient technical skills for any job title")

    if blockchain_languages_known:
        job_title += f" / Blockchain Developer ({', '.join(blockchain_languages_known)})"
        reasons.append(f"Is also a Blockchain Developer specializing in {', '.join(blockchain_languages_known)}")
        rating += 3

    experience_match = re.search(r'(\d+)[+~><]* year', text, re.IGNORECASE)
    if experience_match:
        experience_str = experience_match.group(1)
        if experience_str.isnumeric():
            total_experience_years = int(experience_str)
            reasons.append(f"Has {total_experience_years} years of experience")
    else:
        rejection_reasons.append("No experience information found")

    if total_experience_years >= 7:
        rating += 3
    elif total_experience_years >= 4:
        rating += 2
    elif total_experience_years >= 1:
        rating += 1
    else:
        rejection_reasons.append("Insufficient years of experience")

    rating = min(10, rating)
    
    return list(skills), job_title, total_experience_years, rating, reasons, rejection_reasons

if __name__ == "__main__":
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/1_Thomas_Beckford_Resume_2023-a4554e111005df54c256dc7b4252d20d.pdf"
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, job_title, total_experience_years, rating, reasons, rejection_reasons = analyze_freelancer(text)
        
        print(f"Skills: {list(set(skills))}")
        print(f"Job Title: {job_title}")
        print(f"Total Years of Experience: {total_experience_years}")
        print(f"Rating: {rating}")
        print("Reasons for Rating:")
        for reason in reasons:
            print(f"  - {reason}")

        if rating >= 8:
            print("Recommendation: Strongly consider for Everbuild talent pool.")
        elif rating >= 5:
            print("Recommendation: Accept into Everbuild talent pool.")
        else:
            print("Recommendation: Reject application.")
            print("Reasons for Rejection:")
            for reason in rejection_reasons:
                print(f"  - {reason}")
    else:
        print("Failed to extract text from PDF.")
