
# JobHubSA – Job Recruitment Platform

JobHubSA is a web platform designed to connect job seekers with employment opportunities, mentorship, and professional development resources. The platform was created to explore ways technology can help address youth unemployment by providing access to jobs, learning resources, and career guidance.
Live demo: https://jobhubsa.onrender.com/

## Features

- User registration and authentication
- Job listing and job application functionality
- Job filtering by category and location
- Mentor discovery for career guidance
- Course discovery for professional development
- User profile management

## Tech Stack

Backend
- Python
- Flask

Database
- MongoDB
- MongoEngine

Frontend
- HTML
- CSS
- JavaScript
- Bootstrap
- jQuery

## Project Structure

app/
routes/
models/
templates/
static/
wsgi.py
requirements.txt

## Installation

### 1. Clone the repository

git clone https://github.com/ItumelengRandyMalau/flask-job-platform.git

### 2. Navigate into the project directory

cd flask-job-platform

### 3. Create a virtual environment


### 3. Create a virtual environment

python -m venv venv

Activate the environment

Windows:

venv\Scripts\activate


Mac/Linux:



source venv/bin/activate


### 4. Install dependencies

pip install -r requirements.txt


### 5. Configure MongoDB

Update the MongoDB connection URI in the project configuration.

### 6. Run the application

python wsgi.py


The application will run at: http://127.0.0.1:5000


## Future Improvements

- Role-based authentication for employers and job seekers
- Job recommendation system
- Application tracking dashboard
- Cloud deployment improvements

## Developers

This project was initially developed as a collaborative effort and is currently being improved and maintained.

- Itumeleng Malau – Backend Developer  
- Leeon Kariuki – Backend Developer  
- Lawrence Mokoko – Frontend Developer  

## Author

Itumeleng Randy
