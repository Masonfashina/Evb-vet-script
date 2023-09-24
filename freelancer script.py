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
    blockchain_languages_known = []
    job_title = ""
    total_experience_years = 0
    rating = 0
    
    frontend_languages = ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue']
    backend_languages = ['Python', 'Ruby', 'PHP', 'Node.js', 'Java', 'C#', 'Go']
    blockchain_languages = ['Solidity', 'Rust', 'C++', 'Vyper', 'Huff', 'Go (Golang)']

    
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
            blockchain_languages_known.append(lang)
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
    
    if blockchain_languages_known:
        job_title += f" / Blockchain Developer ({', '.join(blockchain_languages_known)})"
        rating += 3
    
    experience_match = re.search(r'(\d+)[+~><]* year', text, re.IGNORECASE)
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
    
    return list(skills), job_title, total_experience_years, rating

if __name__ == "__main__":
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Eric-Wong-Full-Stack-Blockchain-Engineer-96cda2163268575a98297a19e3d4da0c.pdf"  # Replace with your PDF file path or URL
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, job_title, total_experience_years, rating = analyze_freelancer(text)
        
        print(f"Skills: {list(set(skills))}")
        print(f"Job Title: {job_title}")
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
