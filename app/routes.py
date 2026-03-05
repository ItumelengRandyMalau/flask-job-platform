from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import app
from .models import User, JobPost, Application, Course, UserCourseProgress
from datetime import datetime
from flask_login import LoginManager

login_manager = LoginManager()

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        try:
            user = User(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            user.save()
            login_user(user)
            return redirect(url_for('profile'))
        except Exception as e:
            flash("An error occurred while creating your account. Please try again.")
            print(e)  # Log the error to the console for debugging
    return render_template('signup.html', user=current_user)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.objects(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('profile'))
        flash("Invalid login details.")
    return render_template('login.html', user=current_user)

# Profile route
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Job listings route
@app.route('/jobs')
def job_listings():
    location = request.args.get('location')
    category = request.args.get('category')

    query = {}
    if location:
        query['location__icontains'] = location
    if category:
        query['category__icontains'] = category

    jobs = JobPost.objects(**query)
    return render_template('job_listings.html', jobs=jobs, user=current_user)

# Apply job route
@app.route('/apply/<job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = JobPost.objects(id=job_id).first()
    if job:
        application = Application(user=current_user, job=job)
        application.save()
        return redirect(url_for('job_listings'))
    return 'Job not found', 404

# Route to view a specific job post
@app.route('/job/<job_id>')
def job_detail(job_id):
    job = mongo.db.jobs.find_one({'_id': ObjectId(job_id)})
    return render_template('job_list.html', job=job)

# Mentorship route
@app.route('/mentors')
def mentors():
    mentors = User.objects(is_mentor=True)
    return render_template('mentors.html', mentors=mentors, user=current_user)

# Courses route
@app.route('/courses')
def courses():
    # Creating Courses document
    course = Course(
        title="Software Engineer - Front-end",
        description="This course provides you with the knowledge and exposes you to tools you can use to develop websites effectively.",
        duration=5
    )
    course.save()

    courses = Course.objects()
    return render_template('courses.html', courses=courses, user=current_user)

# Route to get specific course by id
@app.route('/course/<course_id>')
@login_required
def course_detail(course_id):
    course = Course.objects(id=course_id).first()
    progress = UserCourseProgress.objects(user=current_user, course=course).first()
    return render_template('course_detail.html', course=course, progress=progress, user=current_user)

@app.route('/about')
def about():
    return render_template('about.html')  # Ensure you have about.html in your templates folder

@app.route('/contact')
def contact():
    return render_template('contact.html') 

@app.route('/blog')
def blog():
    return render_template('blog.html')  # Ensure blog.html exists in your templates folder

@app.route('/find_job')
def find_job():
    return render_template('find_job.html')  # Make sure 'find_job.html' exists

@app.route('/employer')
def employer():
    return render_template('employer.html')  # Ensure 'employer.html' exists

/*# Route for the home page (show job listings)
@app.route('/')
def index():
    jobs = mongo.db.jobs.find()  # Get all job posts
    return render_template('index.html', jobs=jobs)

# Route for posting a new job
@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if request.method == 'POST':
        job_title = request.form['title']
        company = request.form['company']
        description = request.form['description']
        
        
        # Insert new job into the database
        mongo.db.jobs.insert_one({
            'title': job_title,
            'company': company,
            'description': description
        })
        return redirect(url_for('index'))
    
    return render_template('post_job.html')

# Route to view a specific job post
@app.route('/job/<job_id>')
def job_detail(job_id):
    job = mongo.db.jobs.find_one({'_id': ObjectId(job_id)})
    return render_template('job_list.html', job=job)*/