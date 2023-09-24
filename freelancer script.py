import re
import PyPDF2
import requests
import io
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

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
    
    # Tokenize the text
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    
    frontend_languages = ['html', 'css', 'javascript', 'react', 'angular', 'vue']
    backend_languages = ['python', 'ruby', 'php', 'node.js', 'java', 'c#', 'go']
    blockchain_languages = ['solidity', 'rust', 'c++', 'vyper', 'huff', 'go']
    identified_soft_skills = ['communication', 'teamwork', 'problem-solving', 'leadership']
    
    for word in filtered_words:
        if word in frontend_languages:
            skills.add(word.capitalize())
            rating += 0.5
        if word in backend_languages:
            skills.add(word.capitalize())
            rating += 1
        if word in blockchain_languages:
            skills.add(word.capitalize())
            rating += 1.5
        if word in identified_soft_skills:
            soft_skills.add(word.capitalize())
            rating += 0.5
    
    if skills.intersection(set(frontend_languages)) and skills.intersection(set(backend_languages)):
        job_title = "Fullstack Developer"
        rating += 2
    elif skills.intersection(set(frontend_languages)):
        job_title = "Frontend Developer"
        rating += 1
    elif skills.intersection(set(backend_languages)):
        job_title = "Backend Developer"
        rating += 1
    
    if skills.intersection(set(blockchain_languages)):
        job_title += " / Blockchain Developer"
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
    
    return list(skills), list(soft_skills), job_title, total_experience_years, rating

if __name__ == "__main__":
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Resume-Matthew-Hicks-2023-13b46b1c590c9630ebcc342909b3a79f.pdf"  # Replace with your PDF file path or URL
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, soft_skills, job_title, total_experience_years, rating = analyze_freelancer(text)
        
        print(f"Skills: {skills}")
        print(f"Soft Skills: {soft_skills}")
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
