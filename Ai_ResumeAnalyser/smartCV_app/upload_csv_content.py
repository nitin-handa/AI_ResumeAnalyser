import pandas
from models import skills_dataset
df=pandas.read_csv('smartCV_app/skillsss.csv')
df['skills']=df['supply chain engineering\n']
obj=skills_dataset(skill='supply chain engineering')
obj.save()
for i in df['skills']:
    obj=skills_dataset(skill=i)
    obj.save()
