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
    stacks = set()
    job_title = ""
    experience_level = ""
    total_experience_years = 0
    final_rating = 0
    
    # Skill Rating
    skill_rating = 0
    if re.search(r'react', text, re.IGNORECASE):
        skills.add("React")
        skill_rating += 10
    if re.search(r'node\.?js', text, re.IGNORECASE):
        skills.add("Node.js")
        skill_rating += 10
    if re.search(r'blockchain', text, re.IGNORECASE):
        skills.add("Blockchain")
        skill_rating += 20
    if re.search(r'web3', text, re.IGNORECASE):
        skills.add("Web3")
        skill_rating += 20
    
    # Stack Rating
    stack_rating = 0
    if skill_rating >= 30:
        stacks.add("Full Stack Developer")
        stack_rating += 20
    elif skill_rating >= 20:
        stacks.add("Web3 / Blockchain / Smart Contract Developer")
        stack_rating += 15
    elif skill_rating >= 10:
        stacks.add("Front-end or Back-end Developer")
        stack_rating += 10
    
    # Job Title Rating
    job_title_rating = 0
    if re.search(r'junior\s*developer|entry\s*level', text, re.IGNORECASE):
        job_title = "Junior Developer"
        job_title_rating += 5
    elif re.search(r'senior\s*developer|lead\s*developer', text, re.IGNORECASE):
        job_title = "Senior Developer"
        job_title_rating += 15
    else:
        job_title = "Mid-level Developer"
        job_title_rating += 10
        
    # Experience Rating
    experience_rating = 0
    experience_years = re.findall(r'(\d+)\s*years?\s*experience', text, re.IGNORECASE)
    experience_years = [int(year) for year in experience_years]

    if experience_years:
        total_experience_years = sum(experience_years)
    
        if total_experience_years >= 7:
            experience_level = "Senior"
            experience_rating += 20
        elif total_experience_years >= 4:
            experience_level = "Mid-level"
            experience_rating += 15
        else:
            experience_level = "Junior"
            experience_rating += 10

    # Final Rating
    final_rating = skill_rating + stack_rating + job_title_rating + experience_rating
    
    # Acceptance Criteria
    acceptance = "Reject"
    if final_rating >= 60:
        acceptance = "Strongly Accept"
    elif final_rating >= 50:
        acceptance = "Accept"
    elif final_rating >= 40:
        acceptance = "Consider"

    return list(skills), list(stacks), job_title, experience_level, total_experience_years, final_rating, acceptance

if __name__ == "__main__":
    # Replace this with your PDF file path or URL
    file_path_or_url = "https://www.everbuild.pro/wp-content/uploads/wpforms/946-07b67c26f764cc6be3b22e721ea31a5c/Cody-Lund-dcdc972b9744f152fbbf0b8d334c2085.pdf"
    
    text = extract_text_from_pdf(file_path_or_url)
    
    if text:
        skills, stacks, job_title, experience_level, total_experience_years, final_rating, acceptance = analyze_freelancer(text)
        
        print(f"Skills: {skills}")
        print(f"Stacks: {stacks}")
        print(f"Job Title: {job_title}")
        print(f"Experience Level: {experience_level}")
        print(f"Total Years of Experience: {total_experience_years}")
        print(f"Final Rating: {final_rating}")
        print(f"Acceptance: {acceptance}")
    else:
        print("Failed to extract text from PDF.")
