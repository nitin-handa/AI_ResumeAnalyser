

```markdown
# Resume Builder and Skills Matching Application

This Django-based application allows users to upload their resumes and job descriptions, extract relevant skills, and compare them to find matching skills. Additionally, the application provides recommendations for skills that are relevant to the job description but not present in the resume. 

# Features

- Custom Algorithms: This application is built purely on custom algorithms without relying on any external APIs or services for information extraction.
- Resume and Job Description Parsing: Extracts key information such as skills, experience, education, and more from uploaded resumes and job descriptions.
- Skills Comparison: Compares the skills extracted from the resume with those in the job description and identifies matching and missing skills.
- Skills Recommendation: Provides recommendations for skills that are relevant to the job description but not present in the resume.
- Multiple Skills Datasets: Supports the management of multiple skills datasets, allowing for the storage of different skill sets in separate folders.
- Admin Portal: Manage skills datasets and other data through the Django admin portal.
- Secure File Upload: Upload and manage resumes, job descriptions, and skills datasets securely.

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nitin-handa/AI_ResumeAnalyser/.git
   cd AI_ResumeAnalyser
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply the migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser for the Django admin portal:
   ```bash
   python manage.py c
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application by visiting `http://127.0.0.1:8000/` in your web browser.

## How It Works

1. **Upload Resumes and Job Descriptions**: Users can upload their resumes and job descriptions through the web interface.
2. **Skills Extraction**: The application extracts skills and other relevant information from the uploaded documents.
3. **Skills Matching**: The application compares the extracted skills from the resume with those in the job description and displays the results.
4. **Skills Recommendation**: Based on the job description, the application recommends additional skills that may enhance the user's profile.

## Database Tables and Extracted Information

The application uses several database tables to store and manage the extracted information. Below are the key tables and the information they hold:

### 1. `ResumeData`
- **Purpose**: Stores detailed information extracted from resumes and job descriptions.
- **Fields**:
  - `resume_text`: The full text of the uploaded resume.
  - `job_description_text`: The full text of the uploaded job description.
  - `experience`: JSON field storing the extracted experience details.
  - `contact_number`: The contact number extracted from the resume.
  - `linkedin_account`: LinkedIn profile link extracted from the resume.
  - `github_account`: GitHub profile link extracted from the resume.
  - `email`: Email address extracted from the resume.
  - `education`: JSON field storing the extracted education details.
  - `resume_skills`: JSON field storing the skills extracted from the resume.
  - `job_description_skills`: JSON field storing the skills extracted from the job description.
  - `matching_skills`: JSON field storing the skills that match between the resume and job description.
  - `missing_skills`: JSON field storing the skills missing from the resume but present in the job description.
  - `matching_percentage`: The percentage of skills that match between the resume and job description.
  - `job_field`: The field or industry related to the job description.
  - `job_profile`: The job profile title extracted from the job description.

### 2. `SelectedSkills`
- **Purpose**: Tracks the skills selected by users for further processing.
- **Fields**:
  - `resume_serial_number`: Links to the `ResumeData` entry.
  - `skill`: JSON field storing the list of selected skills.
  - `selected`: Boolean field indicating whether the skill was selected by the user.

### 3. `Logging`
- **Purpose**: Logs significant actions or events within the application.
- **Fields**:
  - `serial_number`: A reference number for the log entry.
  - `timestamp`: The date and time when the event occurred.
  - `message`: A detailed description of the logged event.

### 4. `UploadedPdf`
- **Purpose**: Stores metadata about the PDFs uploaded by users.
- **Fields**:
  - `serial_number`: A reference number for the uploaded PDF.
  - `pdf`: The file path to the uploaded PDF.
  - `uploaded_at`: The timestamp when the PDF was uploaded.

### 5. `csv_file`
- **Purpose**: Manages the uploading of skills datasets in CSV format.
- **Fields**:
  - `file`: The file path to the uploaded CSV file.

### 6. `skills_dataset`
- **Purpose**: Stores individual skills extracted from the uploaded CSV files.
- **Fields**:
  - `skill`: The name of the skill.

## CSRF Protection

This application includes CSRF protection for secure form submissions. Ensure that your browser accepts cookies, and that the CSRF token is properly included in forms.

## Contribution

Contributions are welcome! Feel free to submit issues, fork the repository, and send pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
