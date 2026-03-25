from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import app
from .models import User, JobPost, Application, Course, UserCourseProgress
from datetime import datetime
from decimal import Decimal, InvalidOperation
from flask import abort
from flask import send_file
import io

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form

        password = data['password']
        confirm_password = data['confirm_password']

        # PASSWORD CHECK
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('signup'))

        try:
            role = data.get('role')

            user = User(
            username=data.get('username'),
            email=data.get('email'),
            company=data.get('company'),
            location=data.get('location'),
            cellphone=data.get('cellphone'),
            role=role,
            is_employer=(role == "employer"),
            is_job_seeker=(role == "job_seeker"),
            is_mentor=(role == "mentor")
            )

            user.set_password(password)
            user.save()

            login_user(user)

            if user.role == "employer":
                return redirect(url_for('dashboard'))

            elif user.role == "mentor":
                return redirect(url_for('mentors'))

            else:
                return redirect(url_for('job_listings'))

        except Exception as e:
            flash("An error occurred while creating your account.", "danger")
            print(e)

    return render_template('signup.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.objects(email=request.form['email']).first()

        if user and user.check_password(request.form['password']):
            login_user(user)
            if user.role == "employer":
                return redirect(url_for('dashboard'))
            
            elif user.role == "mentor":
                return redirect(url_for('mentors'))

            else:
                return redirect(url_for('job_listings'))

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


@app.route('/apply/<job_id>', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    job = JobPost.objects(id=job_id).first()

    if current_user.role != "job_seeker":
        flash("Only job seekers can apply", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        file = request.files.get('cv')

        if not file or file.filename == '':
            flash("Please upload your CV", "danger")
            return redirect(request.url)

        # Check if already applied
        existing = Application.objects(job=job, user=current_user).first()
        if existing:
            flash("You already applied for this job", "warning")
            return redirect(url_for('job_listings'))

        # Create application
        application = Application(
            job=job,
            user=current_user._get_current_object()
        )

        # file handling
        application.cv = file

        application.save()

        flash("Application submitted successfully!", "success")
        return redirect(url_for('job_listings'))

    return render_template('apply.html', job=job)

@app.route('/view_cv/<app_id>')
@login_required
def view_cv(app_id):
    application = Application.objects(id=app_id).first()

    if not application or not application.cv:
        flash("CV not found", "danger")
        return redirect(url_for('dashboard'))

    return send_file(
        io.BytesIO(application.cv.read()),
        download_name=application.cv.filename or "cv.pdf",
        as_attachment=True
    )


@app.route('/job/<job_id>')
def job_detail(job_id):

    job = JobPost.objects(id=job_id).first()

    return render_template('job_detail.html', job=job)


@app.route('/courses')
def courses():

    courses = Course.objects()

    return render_template('courses.html', courses=courses, user=current_user)

@app.route('/employer', methods=['GET', 'POST'])
def employer():

    if request.method == 'POST':

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # PASSWORD VALIDATION
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for('employer'))

        try:
            user = User(
                username=request.form['fullname'],
                email=request.form['email'],
                role="employer",
                company=request.form['company'],
                cellphone=request.form['cellphone'],
                location=request.form['location']
            )

            user.set_password(password)
            user.save()

            login_user(user)

            return redirect(url_for('dashboard'))

        except Exception as e:
            flash("Error creating employer account", "danger")
            print(e)

    return render_template('employer.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/mentors')
def mentors():

    mentors = User.objects(role="mentor")

    return render_template('mentors.html', mentors=mentors)

@app.route('/dashboard')
@login_required
def dashboard():

    if current_user.role != "employer":
        abort(403)

    if current_user.role == "job_seeker":
        return redirect(url_for('profile'))

    jobs = JobPost.objects(employer=current_user._get_current_object()
    )

    return render_template('dashboard.html', jobs=jobs)

@app.route('/post_job', methods=['GET', 'POST'])
@login_required
def post_job():

    if current_user.role != "employer":
        abort(403)

    if request.method == 'POST':

        job = JobPost(
            title=request.form['title'],
            company=request.form['company'],
            location=request.form['location'],
            description=request.form['description'],
            category=request.form['category'],
            salary=request.form.get('salary'),

            employer=current_user._get_current_object() 
        )

        job.save()

        flash("Job posted successfully", "success")
        return redirect(url_for('dashboard'))

    return render_template('post_job.html')

@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):

    if current_user.role != "employer":
        abort(403)

    job = JobPost.objects(id=job_id).first()

    if not job:
        abort(404)

    if job.employer != current_user._get_current_object():
        abort(403)

    if request.method == 'POST':

        job.title = request.form['title']
        job.company = request.form['company']
        job.location = request.form['location']
        job.description = request.form['description']

        job.save()

        flash("Job updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('edit_job.html', job=job)

@app.route('/delete_job/<job_id>', methods=['POST'])
@login_required
def delete_job(job_id):

    if current_user.role != "employer":
        abort(403)

    job = JobPost.objects(id=job_id).first()

    if not job:
        flash("Job not found", "danger")
        return redirect(url_for('dashboard'))

    # ensure employer owns the job
    if job.employer != current_user._get_current_object():
        abort(403)

    job.delete()

    flash("Job deleted successfully", "success")
    return redirect(url_for('dashboard'))

@app.route('/job_applications/<job_id>')
def job_applications(job_id):

    job = JobPost.objects(id=job_id).first()

    applications = Application.objects(job=job)

    return render_template('applications.html', job=job, applications=applications)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/job/<job_id>/applications')
@login_required
def view_applications(job_id):

    if current_user.role != "employer":
        abort(403)

    job = JobPost.objects(id=job_id).first()

    if not job:
        abort(404)

    if job.employer != current_user:
        abort(403)

    applications = Application.objects(job=job)

    return render_template(
        'applications.html',
        job=job,
        applications=applications
    )

@app.route('/my_applications')
@login_required
def my_applications():
    applications = Application.objects(user=current_user)

    return render_template(
        'applications.html',
        applications=applications,
        job=None
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')