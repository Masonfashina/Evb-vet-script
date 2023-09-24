import re
import PyPDF2
import requests
import io
import nltk
from nltk.tokenize import word_tokenize

# Download the punkt tokenizer
nltk.download('punkt', quiet=True)

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
    soft_skills = set()
    job_title = ""
    total_experience_years = 0
    rating = 0
    feedback = []
    
    frontend_languages = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'NextJS', 'Redux']
    backend_languages = ['Python', 'Ruby', 'PHP', 'Node.js', 'Java', 'C#', 'Go']
    blockchain_languages = ['Solidity', 'Rust', 'C++', 'Vyper', 'Huff', 'Go (Golang)']
    certifications = ['AWS Certified', 'Certified Ethical Hacker', 'Google Associate Cloud Engineer', 'Microsoft Certified', 'Cisco Certified']
    
    # Tokenize the text for NLP analysis
    tokens = word_tokenize(text.lower())
    soft_skills_list = ['teamwork', 'communication', 'problem-solving', 'leadership', 'adaptability']
    
    for skill in soft_skills_list:
        if skill in tokens:
            soft_skills.add(skill.capitalize())
            rating += 0.5
    
    for cert in certifications:
        if re.search(rf'\b{cert}\b', text, re.IGNORECASE):
            feedback.append(f"Has certification: {cert}")
            rating += 1
    
    for lang in frontend_languages:
        if re.search(rf'\b{lang}\b', text, re.IGNORECASE):
            skills.add(lang)
            rating += 0.5
    
    for lang in backend_languages:
        if re.search(rf'\b{lang}\b', text, re.IGNORECASE):
            skills.add(lang)
            rating += 1
    
    for lang in blockchain_languages:
        if re.search(rf'\b{lang}\b', text, re.IGNORECASE):
            skills.add(lang)
            rating += 1.5
    
    if skills.intersection(frontend_languages) and skills.intersection(backend_languages):
        job_title = "Fullstack Developer"
        rating += 2
    elif skills.intersection(frontend_languages):
        job_title = "Frontend Developer"
        rating += 1
    elif skills.intersection(backend_languages):
        job_title = "Backend Developer"
        rating += 1
    
    experience_match = re.search(r'(\d+)\s*(?:around|about|over|more than)?[+~><]*\s*year', text, re.IGNORECASE)

    if experience_match:
        experience_str = experience_match.group(1)
        if experience_str.isnumeric():
            total_experience_years = int(experience_str)
    
    if total_experience_years >= 7:
        rating += 3
    elif total_experience_years >= 4:
        rating += 2
    elif total_experience_years >= 1:
        rating += 1
    
    rating = min(10, rating)
    
    if len(skills) == 0 or total_experience_years < 2 or len(soft_skills) == 0:
        recommendation = "Reject application"
        feedback.append("Insufficient skills, experience, or soft skills.")
    else:
        recommendation = "Accept into Everbuild talent pool"
    
    return list(skills), job_title, total_experience_years, rating, recommendation, feedback

if __name__ == "__main__":
    file_path_or_url = "path/to/your/pdf/file.pdf"  # Replace with your PDF file path or URL
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, job_title, total_experience_years, rating, recommendation, feedback = analyze_freelancer(text)
        
        print(f"Skills: {list(set(skills))}")
        print(f"Job Title: {job_title}")
        print(f"Total Years of Experience: {total_experience_years}")
        print(f"Rating: {rating}")
        print(f"Recommendation: {recommendation}")
        if feedback:
            print(f"Feedback: {', '.join(feedback)}")
    else:
        print("Failed to extract text from PDF.")
