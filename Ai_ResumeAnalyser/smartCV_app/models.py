from django.db import models
from datetime import datetime ,timezone

class ResumeData(models.Model):
    id = models.AutoField
    serial_number = models.IntegerField(default=0)
    resume_text = models.TextField(default='')
    job_description_text = models.TextField(default='')
    experience = models.JSONField(default=list)
    # experience = models.TextField(default='')
    contact_number = models.CharField(default='', max_length=13)
    linkedin_account = models.CharField(default='',max_length=100)
    github_account = models.CharField(default='',max_length=100)
    email = models.CharField(default='',max_length=100)
    # education = models.TextField(default='')
    education = models.JSONField(default=list)
    resume_skills = models.JSONField(default=list)
    job_description_skills = models.JSONField(default=list)
    matching_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    # resume_skills = models.TextField(default='')
    # job_description_skills = models.TextField(default='')
    # matching_skills = models.TextField(default='')
    # missing_skills = models.TextField(default='')
    matching_percentage = models.FloatField(default=0.0)
    job_field=models.CharField(default='',max_length=100)
    job_profile=models.CharField(default='',max_length=100)

    def __str__(self) -> str:
        return str(self.serial_number)
    
class SelectedSkills(models.Model):
    id = models.AutoField
    resume_serial_number = models.IntegerField(default=0)
    skill = models.JSONField(default=list)  
    selected = models.BooleanField(default=True)  

    def __repr__(self):
        return f"<SelectedSkill {self.skill}>"
    
    
class Logging(models.Model):
    id = models.AutoField
    serial_number = models.IntegerField()
    timestamp = models.TimeField(default=datetime.now(timezone.utc).astimezone().replace(tzinfo=None))
    message = models.TextField(default='')

    def __repr__(self):
        return f"<Logging {self.timestamp}: {self.message}>"

class UploadedPdf(models.Model):
    serial_number = models.IntegerField(default=0)
    pdf = models.FileField(upload_to='static/pdf_files/',default=None)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pdf)
    
class csv_file(models.Model):
    file= models.FileField(upload_to='static/csv_file/',default=None)

class skills_dataset(models.Model):
    skill=models.TextField()

    def __str__(self) -> str:
        return self.skill
    