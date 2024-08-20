from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
import os
import re
import csv
import pandas as pd
from django.contrib import messages
from django.contrib.auth import authenticate
from itertools import count
from datetime import datetime, timezone
from .models import ResumeData,Logging,SelectedSkills,UploadedPdf,skills_dataset
from pdfminer.high_level import extract_text
from docx import Document
import PyPDF2
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse


@csrf_exempt
def get_resume_content(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serial_number = data.get('serial_number')
        
        try:
            resume = UploadedResume.objects.get(serial_number=serial_number)
            file_type = resume.file.name.split('.')[-1].lower()
            file_url = resume.file.url
            
            return JsonResponse({
                'success': True, 
                'file_type': file_type,
                'file_url': file_url
            })
        except UploadedResume.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Resume not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def up_data(request):
    df=pd.read_csv('smartCV_app/skillsss.csv')
    # df=pd.read_csv('smartCV_app/skills.csv')
    df['skills']=df['supply chain engineering\n']
    obj=skills_dataset(skill='supply chain engineering')
    obj.save()
    for i in df['skills']:
        obj=skills_dataset(skill=i[:-1])
        obj.save()
    return HttpResponse('done!')


def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path)
    except Exception as e:
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return ""
    
def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error extracting text from DOCX '{docx_path}': {e}")
        return ""


# def extract_text_from_txt(file_path):
#     with open(file_path, 'r') as file:
#         text = file.read()
#     return text

def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error extracting text from TXT '{txt_path}': {e}")
        return ""


def extract_information_from_resume(text, pattern):
    try:
        match = re.search(pattern, text)
        return match.group() if match else ""
    except Exception as e:
        print(f"Error extracting information: {e}")
        return ""

def extract_experience_from_resume(text):
    experiences = []
    experience_patterns = [
        r"\b\d{1,2}\s?(?:-|to)\s?\d{1,2}\s(?:years?|yrs?)\s(?:of\s)?(?:experience|exp)",
        r"\b(?:[1-9][0-9]?|100)\s(?:years?|yrs?)\s(?:of\s)?(?:experience|exp)",
        r"\b(?:[1-9][0-9]?|100)\s(?:months?|mos?)\s(?:of\s)?(?:experience|exp)",
        r"\b(?:[1-9][0-9]?|100)\+\s(?:years?|yrs?)\s(?:of\s)?(?:experience|exp)"
    ]
    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            experiences.append(match.strip())
    return experiences

def extract_contact_number_from_resume(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    return extract_information_from_resume(text, pattern)

def extract_linkedin_account_from_resume(text):
    pattern = r"(?i)\b(?:https?://)?(?:www\.)?linkedin\.com/(?:in|profile)/[\w-]+/?"
    return extract_information_from_resume(text, pattern)

def extract_github_account_from_resume(text):
    pattern = r"(?i)\b(?:https?://)?(?:www\.)?github\.com/[\w-]+/?"
    return extract_information_from_resume(text, pattern)

def extract_email_from_resume(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return extract_information_from_resume(text, pattern)

def extract_education_from_resume(text):
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBTech\b|\bB\.Tech\b|\bB\.Tech\.\s*\(?\s*Computer\s*Science\s*And\s*Engineering\s*\)?)"
    return re.findall(pattern, text)

def extract_skills_from_resume(text, skills_csv):
    skills = []
    try:
        with open(skills_csv, newline='', encoding='utf-8') as csvfile:
            reader = skills_dataset.objects.all()
            skills_list = [row.skill.strip() for row in reader]  # Strip newline characters
    except Exception as e:
        print("Error reading skills CSV:", e)
        return skills

    # Iterate over skills list
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match and skill.strip():  # Only add non-empty skills
            # Filter out numeric values
            if not any(char.isdigit() for char in skill):
                skills.append(skill.strip())

    return [skill for skill in skills if skill]  # Remove any remaining empty strings

def extract_skills_from_job_description(job_description_text, skills_csv):
    skills = []

    try:
        with open(skills_csv, newline='', encoding='utf-8') as csvfile:
            reader = skills_dataset.objects.all()
            skills_list = [row.skill.strip() for row in reader]
    except Exception as e:
        print("Error reading skills CSV:", e)
        return skills

    # Iterate over skills list
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, job_description_text, re.IGNORECASE)
        if match and skill.strip():  # Only add non-empty skills
            # Filter out numeric values
            if not any(char.isdigit() for char in skill):
                skills.append(skill.strip())

    return [skill for skill in skills if skill]  # Remove any remaining empty strings

def calculate_matching_percentage(resume_skills, job_description_skills):
    try:
        if job_description_skills:
            common_skills = set(resume_skills).intersection(job_description_skills)
            matching_skills=(len(common_skills) / len(job_description_skills)) * 100
            matching_skills = round(matching_skills, 1)
            return matching_skills
        else:
            return 0
    except Exception as e:
        print(f"Error calculating matching percentage: {e}")
        return 0


def calculate_matching_skills(resume_skills, job_description_skills):
    # Find common skills between resume skills and job description skills
    common_skills = set(resume_skills).intersection(job_description_skills)

    return list(common_skills)

def calculate_matching_and_missing_skills(resume_skills, job_description_skills):
    resume_skills = [str(i).strip() for i in resume_skills if i.strip()]
    job_description_skills = [str(i).strip() for i in job_description_skills if i.strip()]

    common_skills = list(set(resume_skills).intersection(job_description_skills))
    missing_skills = list(set(job_description_skills).difference(common_skills))

    return [common_skills, missing_skills]

def fetch_auth_page(request):
    return render(request,'fetch_data.html')

def authSuperUser(u_id,u_pass):
    try:
        user=authenticate(username=u_id, password=u_pass)
        if user:
            if user.is_superuser:
                return True
        return False
    except Exception as e:
        print(e)
        return False

def fetchData(request):
    # Use this function to fetch data from database
    try:
        id=request.POST.get('s_id')
        pas=request.POST.get('s_pass')
        if not authSuperUser(u_id=id,u_pass=pas):
            return HttpResponse('SuperUserNotFound!')
        data=ResumeData.objects.all()
        data_base={'serial_number':[],
        'resume_text': [],
        'job_description_text' :[],
        'experience':[],
        'contact_number':[],
        'linkedin_account':[],
        'github_account':[],
        'email':[],
        'education':[],
        'resume_skills':[],
        'job_description_skills':[],
        'matching_skills':[],
        'missing_skills':[],
        'matching_percentage':[],
        'job_field':[],
        'job_profile':[]}
        for i in data:
            data_base['serial_number'].append(i.serial_number)
            data_base['resume_text'].append(i.resume_text)
            data_base['job_description_text'].append(i.job_description_text)
            data_base['experience'].append(i.experience)
            data_base['contact_number'].append(i.contact_number)
            data_base['linkedin_account'].append(i.linkedin_account)
            data_base['github_account'].append(i.github_account)
            data_base['email'].append(i.email)
            data_base['education'].append(i.education)
            data_base['resume_skills'].append(i.resume_skills)
            data_base['job_description_skills'].append(i.job_description_skills)
            data_base['matching_skills'].append(i.matching_skills)
            data_base['missing_skills'].append(i.missing_skills)
            data_base['matching_percentage'].append(i.matching_percentage)
            data_base['job_field'].append(i.job_field)
            data_base['job_profile'].append(i.job_profile)
        df=pd.DataFrame.from_dict(data_base)
        df.to_csv('Resume-data.csv')
        return HttpResponse('Success!')
    except Exception as e:
        return HttpResponse(f'{e}')

def index(request):
    job_fields = [
    "Accounting and Finance",
    "Administrative and Office Support",
    "Arts, Design, and Entertainment",
    "Business and Management",
    "Construction and Extraction",
    "Education and Training",
    "Engineering and Architecture",
    "Healthcare and Medical",
    "Hospitality and Tourism",
    "Information Technology (IT)",
    "Legal",
    "Manufacturing and Production",
    "Marketing and Sales",
    "Media and Communication",
    "Public Safety and Security",
    "Science and Research",
    "Skilled Trades",
    "Social Services",
    "Transportation and Logistics",
    "Agriculture and Natural Resources",
    "Real Estate"
    ]
    return render(request,'index.html',{'job_fields':job_fields})


def upload_files(serial_number, files):
    names = []
    for i in files:
        u = UploadedPdf(serial_number=serial_number, pdf=i)
        u.save()
        name = u.__str__()
        # Use os.path.normpath to normalize the path for the current OS
        name = os.path.normpath(name)
        names.append(name)
    return names


def uploadResume(request):
    try:
        inputFormat = request.POST.get('inputFormat')
        serial_number = ResumeData.objects.all().count() + 1
        if inputFormat == 'document':
            resume_file = request.FILES.get('resume')
            jd_file = request.FILES.get('job_description')
            names = upload_files(serial_number=serial_number, files=[resume_file, jd_file])
            
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resume_path = os.path.normpath(os.path.join(base_dir, names[0]))
            jd_path = os.path.normpath(os.path.join(base_dir, names[1]))
            
            resume_text = extract_text_from_file(resume_path)
            job_description_text = extract_text_from_file(jd_path)
        else:
            resume_text = request.POST.get('resumeText')
            job_description_text = request.POST.get('jobDescriptionText')
        
        job_field = request.POST.get('jobField')
        job_profile = request.POST.get('jobProfile').lower()
        
        skills_csv = os.path.join(os.path.dirname(__file__), 'skillsss.csv')
    
        # Data extraction from text
        extracted_experience = extract_experience_from_resume(resume_text)
        extracted_contact_number = extract_contact_number_from_resume(resume_text)
        linkedin_account = extract_linkedin_account_from_resume(resume_text)
        github_account = extract_github_account_from_resume(resume_text)
        extracted_email = extract_email_from_resume(resume_text)
        extracted_education = extract_education_from_resume(resume_text)
        extracted_resume_skills = extract_skills_from_resume(resume_text, skills_csv)
        extracted_resume_skills = list(set(filter(None, extracted_resume_skills)))
        extracted_job_desc_skills = extract_skills_from_job_description(job_description_text, skills_csv)
        extracted_job_desc_skills = list(set(filter(None, extracted_job_desc_skills)))
        matching_skills, missing_skills = calculate_matching_and_missing_skills(extracted_resume_skills, extracted_job_desc_skills)
        matching_percentage = calculate_matching_percentage(extracted_resume_skills, extracted_job_desc_skills)
    
        # Adding data to database        
        resume_data = ResumeData(
            serial_number=serial_number,
            resume_text=resume_text,
            job_description_text=job_description_text,
            experience=extracted_experience,
            contact_number=extracted_contact_number,
            linkedin_account=linkedin_account,
            github_account=github_account,
            email=extracted_email,
            education=extracted_education,
            resume_skills=[str(i) for i in extracted_resume_skills],
            job_description_skills=extracted_job_desc_skills,
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            matching_percentage=matching_percentage,
            job_field=job_field,
            job_profile=job_profile
        )
        resume_data.save()
        log_message = f"Resume uploaded by user with serial number: {serial_number}"
        log_entry = Logging(message=log_message, serial_number=serial_number)
        log_entry.save()
    
        results = {
            'matching_percentage': matching_percentage,
            'matching_skills': matching_skills,
            'recommend_skills': missing_skills,
            'resume_skills': extracted_resume_skills,
            'serial_number': serial_number,
        }
        
        return render(request=request, template_name='results.html', context=results) 

    except Exception as e:
        print(e)
        return HttpResponse(f'Unable to process your request due to {e} \nPlease go back to homepage and try again!')
    
def extract_text_from_file(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    if file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext == '.docx':
        return extract_text_from_docx(file_path)
    elif file_ext == '.txt':
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f'Unsupported file type: {file_ext}')

def further_results(serial_number,unselected_skills,selected_skills):
    resume_data = ResumeData.objects.filter(serial_number=serial_number).first()
    if resume_data:
        
        # Calculate updated matching percentage
        matching_skills_with_selected = list(resume_data.matching_skills) + list(selected_skills)
        # print("Matched Skills with Job Description (including selected skills):", matching_skills_with_selected)
        # print("matching_skills", resume_skills)
        # print("selected_skills", selected_skills)
        # print("unselected_skills", updated_job_description_skills)
        # print("job_description_skills",job_description_skills)
        # print(resume_data.job_description_skills)
        # print(matching_skills_with_selected)
        # print(unselected_skills)
        
        # Calculate the updated matching percentage
        if resume_data.job_description_skills:
            updated_matching_percentage = (len(matching_skills_with_selected) / len(resume_data.job_description_skills)) * 100
            updated_matching_percentage = round(updated_matching_percentage, 1)  # Round to one decimal place

        else:
            updated_matching_percentage = 0

        # Render the further_results.html template with the necessary data
        return {'resume_data':resume_data, 
                'selected_skills':list(selected_skills),
                'unselected_skills':list(unselected_skills),
                'updated_matching_percentage':updated_matching_percentage,
                'matching_skills_with_selected':matching_skills_with_selected}
    else:
        return {"Resume data not found.": 404}

# def saveSkills(request):
#     try:
#         # Get the serial number of the resume from the request
#         serial_number = int(request.POST.get('serial_number'))
#         selected_skills = request.POST.get('selected_skills[]')
#         unselected_skills = request.POST.get('unselected_skills[]')
        
#         # Check if any skills were selected
#         if not selected_skills:
#             resume_data = ResumeData.objects.filter(serial_number=serial_number).first()
#             if resume_data:
#                 # If no skills are selected, re-render the page without making any changes
#                 res = further_results(
#                     serial_number=serial_number,
#                     unselected_skills=unselected_skills.split(',') if unselected_skills else [],
#                     selected_skills=[]
#                 )
#                 return render(request, 'further_results.html', res)
#             else:
#                 return HttpResponse("Resume data not found. 404")
        
#         # Proceed with the existing logic if skills were selected
#         resume_data = ResumeData.objects.filter(serial_number=serial_number)
#         if resume_data:
#             existing_skills = SelectedSkills.objects.filter(resume_serial_number=serial_number)
#             for skill in existing_skills:
#                 if skill.skill in selected_skills:
#                     skill.selected = True
#                 else:
#                     skill.selected = False

#             # Add new entries for skills not already in the database
#             new_skills = [skill for skill in selected_skills.split(',') if skill not in [s.skill for s in existing_skills]]

#             for skill in new_skills:
#                 selected = skill in selected_skills
#                 new_skill = SelectedSkills(resume_serial_number=serial_number, skill=skill, selected=selected)
#                 new_skill.save()

#             # Pass job_description_skills directly in the URL
#             res = further_results(serial_number=serial_number, unselected_skills=unselected_skills.split(','), selected_skills=new_skills)
#             if "Resume data not found." in res.keys():
#                 return HttpResponse("Resume data not found. 404")
#             return render(request, 'further_results.html', res)
#         else:
#             return HttpResponse("Resume data not found. 404")
#     except Exception as e:
#         return HttpResponse(f"Error: {e}. 500")





def saveSkills(request):
    try:
        # Get the serial number of the resume from the request
        serial_number = int(request.POST.get('serial_number'))
        selected_skills = request.POST.get('selected_skills[]')
        unselected_skills = request.POST.get('unselected_skills[]')

        # Ensure that selected_skills and unselected_skills are lists of valid skills
        if selected_skills:
            selected_skills = [skill.strip() for skill in selected_skills.split(',') if len(skill.strip()) > 1]
        else:
            selected_skills = []

        if unselected_skills:
            unselected_skills = [skill.strip() for skill in unselected_skills.split(',') if len(skill.strip()) > 1]
        else:
            unselected_skills = []

        # Check if any valid skills were selected
        if not selected_skills:
            resume_data = ResumeData.objects.filter(serial_number=serial_number).first()
            if resume_data:
                # If no valid skills are selected, re-render the page without making any changes
                res = further_results(
                    serial_number=serial_number,
                    unselected_skills=unselected_skills,
                    selected_skills=[]
                )
                return render(request, 'further_results.html', res)
            else:
                return HttpResponse("Resume data not found. 404")
        
        # Proceed with updating or adding the skills
        resume_data = ResumeData.objects.filter(serial_number=serial_number)
        if resume_data:
            existing_skills = SelectedSkills.objects.filter(resume_serial_number=serial_number)
            existing_skill_names = [skill.skill for skill in existing_skills]

            # Update existing skills
            for skill in existing_skills:
                skill.selected = skill.skill in selected_skills
                skill.save()

            # Add new skills that are not already in the database
            new_skills = [skill for skill in selected_skills if skill not in existing_skill_names]
            for skill in new_skills:
                new_skill = SelectedSkills(resume_serial_number=serial_number, skill=skill, selected=True)
                new_skill.save()

            # Render the updated skills on the page
            res = further_results(serial_number=serial_number, unselected_skills=unselected_skills, selected_skills=new_skills)
            if "Resume data not found." in res.keys():
                return HttpResponse("Resume data not found. 404")
            return render(request, 'further_results.html', res)
        else:
            return HttpResponse("Resume data not found. 404")
    except Exception as e:
        return HttpResponse(f"Error: {e}. 500")
