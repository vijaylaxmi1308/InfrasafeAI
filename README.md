# InfraSafeAI

**InfraSafeAI** is an AI-powered Public Infrastructure Accident Reporting and Compensation Management System developed to simplify the process of reporting damaged public infrastructure and improve communication between citizens and government authorities. The platform enables users to report issues such as potholes, damaged roads, broken streetlights, fallen trees, drainage problems, and other public infrastructure hazards by uploading an image along with the location of the incident. Using AI-based image analysis, the system helps classify and validate reports, allowing authorities to prioritize genuine complaints and respond more efficiently.

The primary objective of this project is to reduce the time taken to identify and resolve infrastructure-related problems while ensuring transparency throughout the complaint management process. Citizens can easily register, log in, submit reports, and monitor the status of their complaints, whereas administrators can review submitted reports, verify them, manage emergency cases, and update the progress of each complaint. The integration of AI assists in detecting invalid reports and categorizing issues, reducing manual effort and improving overall efficiency.

The application is built using **Django** as the backend framework, **MongoDB Atlas** as the database for storing user and report information, and **HTML, CSS, JavaScript, and Tailwind CSS** for creating a responsive and user-friendly interface. Image processing and AI functionalities are implemented using **Python**, **OpenCV**, **NumPy**, and **Pillow**. The system also supports location-based reporting, allowing authorities to identify the exact location of reported incidents.

## Features

* Secure user registration and authentication
* Report public infrastructure issues with image uploads
* Location-based incident reporting
* Emergency (SOS) reporting feature
* AI-powered image validation and issue classification
* Complaint status tracking for citizens
* Admin dashboard for monitoring and managing reports
* Categorization of emergency and normal incidents
* Centralized storage of reports using MongoDB Atlas

## Technology Stack

**Frontend**

* HTML
* CSS
* JavaScript
* Tailwind CSS

**Backend**

* Django
* Python

**Database**

* MongoDB Atlas
* MongoEngine

**AI & Image Processing**

* OpenCV
* NumPy
* Pillow

## Installation

Clone the repository:

```bash
git clone https://github.com/vijaylaxmi1308/InfrasafeAI.git
cd InfrasafeAI
```

Create and activate a virtual environment:

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all required dependencies:

```bash
pip install -r requirements.txt
```

Configure your MongoDB Atlas connection string in the project settings before running the application.

Start the development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:

```
http://127.0.0.1:8000/
```

## Project Workflow

1. Users register and log in to the application.
2. Citizens report infrastructure issues by uploading an image and providing the incident location.
3. The uploaded image is processed using AI to identify and classify the reported issue.
4. Report details are securely stored in MongoDB Atlas.
5. Administrators review the submitted reports through the admin dashboard.
6. Complaint status is updated after verification and necessary action.
7. Citizens can monitor the progress of their reports through the system.

## Future Enhancements

* Mobile application support
* Real-time notifications via email and SMS
* AI-based severity prediction for incidents
* Multi-language support

## Project Objective

The main objective of InfraSafeAI is to provide an intelligent, transparent, and efficient platform for reporting public infrastructure issues. By integrating Artificial Intelligence with a full-stack web application, the system minimizes manual verification efforts, accelerates issue resolution, improves communication between citizens and authorities, and contributes towards building smarter and safer cities.

## Author

**Vijaylaxmi K Hiremath**

Computer Science Engineering Student

GitHub: https://github.com/vijaylaxmi1308
