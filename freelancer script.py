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
    skills = []
    job_title = ""
    experience_level = ""
    stacks = []
    
    # Analyzing skills
    frontend_skills = re.findall(r'react|angular|vue', text, re.IGNORECASE)
    backend_skills = re.findall(r'node\.?js|django|python', text, re.IGNORECASE)
    web3_skills = re.findall(r'web\s*3|blockchain|smart\s*contract', text, re.IGNORECASE)
    
    if frontend_skills:
        stacks.append("Front-end Developer")
        skills.extend(frontend_skills)
        
    if backend_skills:
        stacks.append("Back-end Developer")
        skills.extend(backend_skills)
        
    if web3_skills:
        stacks.append("Web3 / Blockchain / Smart Contract Developer")
        skills.extend(web3_skills)
    
    # Analyzing job title
    if re.search(r'junior\s*developer|entry\s*level', text, re.IGNORECASE):
        job_title = "Junior Developer"
    elif re.search(r'senior\s*developer|lead\s*developer', text, re.IGNORECASE):
        job_title = "Senior Developer"
    else:
        job_title = "Mid-level Developer"
        
    # Analyzing experience
    experience_years = re.findall(r'(\d+)\s*years?', text)
    experience_years = [int(year) for year in experience_years]

    if experience_years:
        avg_experience = sum(experience_years) // len(experience_years)
        
        if avg_experience >= 7:
            experience_level = "Senior"
        elif avg_experience >= 4:
            experience_level = "Mid-level"
        else:
            experience_level = "Junior"

        # Remove duplicate skills by converting the list to a set and back to a list
    unique_skills = list(set([skill.lower() for skill in skills]))

    return unique_skills, job_title, experience_level, stacks


if __name__ == "__main__":
    # Replace this with your PDF file path or URL
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Cody-Lund-dcdc972b9744f152fbbf0b8d334c2085.pdf"
    
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, job_title, experience_level, stacks = analyze_freelancer(text)
        
        print(f"Skills: {skills}")
        print(f"Job Title: {job_title}")
        print(f"Experience Level: {experience_level}")
        print(f"Stacks: {stacks}")
    else:
        print("Failed to extract text from PDF.")
