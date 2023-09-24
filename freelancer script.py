import re
import PyPDF2
import requests
import io

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
    job_title = ""
    experience_level = ""
    total_experience_years = 0
    rating = 0
    
    # Analyzing skills
    frontend_skills = re.findall(r'(React|Angular|Vue\.js)', text, re.IGNORECASE)
    backend_skills = re.findall(r'(Node\.js|Django|Python)', text, re.IGNORECASE)
    blockchain_skills = re.findall(r'(Blockchain|Web3)', text, re.IGNORECASE)
    
    for skill in frontend_skills:
        skills.add(skill.lower().capitalize())
    for skill in backend_skills:
        skills.add(skill.lower().capitalize())
    for skill in blockchain_skills:
        skills.add(skill.lower().capitalize())
    
    # Analyzing job title and experience
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
    years = list(set([int(year) for year in years]))
    
    if years:
        total_experience_years = max(years) - min(years)
        
        if total_experience_years >= 7:
            experience_level = "Senior"
        elif total_experience_years >= 4:
            experience_level = "Mid-level"
        else:
            experience_level = "Junior"
    
    if frontend_skills:
        job_title = "Frontend Developer"
    if backend_skills:
        job_title = "Backend Developer"
    if frontend_skills and backend_skills:
        job_title = "Fullstack Developer"
    if blockchain_skills:
        job_title = "Blockchain Developer"
    
    # Rating calculation capped at 10
    rating = min(10, len(skills) + (2 if experience_level == "Senior" else 1 if experience_level == "Mid-level" else 0))
    
    return list(skills), job_title, experience_level, total_experience_years, rating

if __name__ == "__main__":
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Cody-Lund-dcdc972b9744f152fbbf0b8d334c2085.pdf"  # Replace with your PDF file path or URL
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, job_title, experience_level, total_experience_years, rating = analyze_freelancer(text)
        
        print(f"Skills: {list(set(skills))}")
        print(f"Job Title: {job_title}")
        print(f"Experience Level: {experience_level}")
        print(f"Total Years of Experience: {total_experience_years}")
        print(f"Rating: {rating}")
        
        if rating >= 8:
            print("Recommendation: Strongly consider for Everbuild talent pool.")
        elif rating >= 5:
            print("Recommendation: Accept into Everbuild talent pool.")
        else:
            print("Recommendation: Reject application.")
    else:
        print("Failed to extract text from PDF.")
