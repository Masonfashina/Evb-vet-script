import re
import PyPDF2
import requests
import io
import nltk
from nltk.tokenize import word_tokenize

# Download the NLTK punkt package for tokenization, only if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# ... (rest of your code remains the same)

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
    rejection_reasons = []

    frontend_languages = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'TypeScript' 'Next.js' 'NextJs']
    backend_languages = ['Python', 'Ruby', 'PHP', 'Node.js', 'Java', 'C#', 'Go',]
    blockchain_languages = ['Solidity', 'Rust', 'C++', 'Vyper', 'Huff', 'Go (Golang)']
    soft_skills_list = ['communication', 'teamwork', 'problem-solving', 'adaptability', 'accountability', 'remote']

    # Tokenize the text for better matching
    tokens = word_tokenize(text.lower())

    for lang in frontend_languages:
        if lang.lower() in tokens:
            skills.add(lang)
            rating += 1
    
    for lang in backend_languages:
        if lang.lower() in tokens:
            skills.add(lang)
            rating += 1
    
    for lang in blockchain_languages:
        if lang.lower() in tokens:
            skills.add(lang)
            rating += 1.5
    
    for skill in soft_skills_list:
        if skill in tokens:
            soft_skills.add(skill.capitalize())
            rating += 0.5

    experience_match = re.search(r'(\d+)[+~><]* year', text, re.IGNORECASE)
    if experience_match:
        experience_str = experience_match.group(1)
        if experience_str.isnumeric():
            total_experience_years = int(experience_str)

    if total_experience_years >= 2:
        rating += 1
    else:
        rejection_reasons.append("Less than 2 years of experience.")

    if len(soft_skills) >= 1:
        rating += 1
    else:
        rejection_reasons.append("Less than 1 soft skill detected.")

    if len(skills) == 0:
        rejection_reasons.append("No technical skills detected.")

    rating = min(10, rating)

    if skills:
        if skills.intersection(frontend_languages) and skills.intersection(backend_languages):
            job_title = "Fullstack Developer"
        elif skills.intersection(frontend_languages):
            job_title = "Frontend Developer"
        elif skills.intersection(backend_languages):
            job_title = "Backend Developer"
        elif skills.intersection(blockchain_languages):
            job_title = "Blockchain Developer"

    recommendation = "Accept into Everbuild talent pool."
    if len(rejection_reasons) == 3:
        recommendation = f"Reject application. Reasons: {', '.join(rejection_reasons)}"

    return list(skills), list(soft_skills), job_title, total_experience_years, rating, recommendation

if __name__ == "__main__":
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Dwayne_Campbell_Senior_Software_Engineer.docx-a3acfd956c9619e6326b977f2d921f7f.pdf"  # Replace with your PDF file path or URL
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, soft_skills, job_title, total_experience_years, rating, recommendation = analyze_freelancer(text)
        
        print(f"Skills: {skills}")
        print(f"Soft Skills: {soft_skills}")
        print(f"Job Title: {job_title}")
        print(f"Total Years of Experience: {total_experience_years}")
        print(f"Rating: {rating}")
        print(f"Recommendation: {recommendation}")
    else:
        print("Failed to extract text from PDF.")
