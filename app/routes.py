from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import app
from .models import User, JobPost, Application, Course, UserCourseProgress
from datetime import datetime


@app.route('/')
def index():
    """if not current_user.is_authenticated:
     return redirect(url_for('login'))
    return render_template('index.html')"""
    return render_template("index.html")


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
            flash("An error occurred while creating your account.")
            print(e)

    return render_template('signup.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.objects(email=request.form['email']).first()

        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('profile'))

        flash("Invalid login details.")

    return render_template('login.html', user=current_user)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/jobs')
def job_listings():

    location = request.args.get('location')
    category = request.args.get('category')

    query = {}

    if location:
        query['location__icontains'] = location

    if category:
        query['category__icontains'] = category

    ''' jobs = JobPost.objects(**query).order_by('-created_at')'''
    page = int(request.args.get('page', 1))

    per_page = 5

    jobs = JobPost.objects(**query).skip((page-1)*per_page).limit(per_page)

    return render_template('job_listings.html', jobs=jobs, user=current_user)


@app.route('/apply/<job_id>', methods=['POST'])
@login_required
def apply_job(job_id):

    job = JobPost.objects(id=job_id).first()

    if job:
        application = Application(user=current_user, job=job)
        application.save()
        flash("Application submitted successfully!", "success")

    return redirect(url_for('job_listings'))


@app.route('/job/<job_id>')
def job_detail(job_id):

    job = JobPost.objects(id=job_id).first()

    return render_template('job_detail.html', job=job)


@app.route('/courses')
def courses():

    courses = Course.objects()

    return render_template('courses.html', courses=courses, user=current_user)

@app.route('/employer')
def employer():
    return render_template("employer.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/mentors')
def mentors():
    return render_template("mentors.html")

@app.route('/dashboard')
def dashboard():

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    jobs = JobPost.objects(employer=current_user)

    return render_template('dashboard.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():

    if request.method == 'POST':

        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        description = request.form['description']
        category = request.form['category']
        salary = request.form['salary']

        job = JobPost(
            title=title,
            company=company,
            location=location,
            category=request.form['category'],
            description=description,
            salary=request.form['salary'],
            employer=current_user
        )

        job.save()
        flash("Job posted successfully!", "success")

        return redirect(url_for('job_listings'))

    return render_template('post_job.html')

@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = JobPost.objects(id=job_id).first()
    if job.employer != current_user:
        return redirect(url_for('job_listings'))

    if request.method == 'POST':

        job.title = request.form['title']
        job.company = request.form['company']
        job.location = request.form['location']
        job.description = request.form['description']

        job.save()
        flash("Job updated successfully!", "success")
        

        return redirect(url_for('job_listings'))

    return render_template('edit_job.html', job=job)

@app.route('/job_applications/<job_id>')
def job_applications(job_id):

    job = JobPost.objects(id=job_id).first()

    applications = Application.objects(job=job)

    return render_template('applications.html', job=job, applications=applications)