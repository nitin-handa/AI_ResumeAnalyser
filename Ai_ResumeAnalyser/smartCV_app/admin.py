from django.contrib import admin
from .models import ResumeData,Logging,SelectedSkills,UploadedPdf,csv_file,skills_dataset

admin.site.register(ResumeData)
admin.site.register(Logging)
admin.site.register(SelectedSkills)
admin.site.register(UploadedPdf)
admin.site.register(csv_file)
admin.site.register(skills_dataset)
