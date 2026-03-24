from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from mongoengine import (
    Document,
    StringField,
    BooleanField,
    EmailField,
    ListField,
    URLField,
    DecimalField,
    ReferenceField,
    DateTimeField,
    IntField,
    FileField
)

class User(UserMixin, Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="job_seeker")
    company = StringField()
    location = StringField()
    cellphone = StringField()
    is_admin = BooleanField(default=False)
    is_employer = BooleanField(default=False)
    is_mentor = BooleanField(default=False)
    is_job_seeker = BooleanField(default=True )
    skills = ListField(StringField())
    portfolio = URLField()
    courses_completed = ListField(StringField())
    reviews = ListField(StringField())
    mentor_bio = StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class JobPost(Document):
    title = StringField(required=True)
    company = StringField(required=True)
    location = StringField(required=True)
    category = StringField(required=True)
    description = StringField()
    salary = DecimalField()
    employer = ReferenceField(User)
    created_at = DateTimeField(default=datetime.utcnow)



class Application(Document):
    user = ReferenceField(User, required=True)
    job = ReferenceField(JobPost, required=True)
    cv = FileField
    applied_at = DateTimeField(default=datetime.utcnow)


class Course(Document):
    title = StringField(required=True)
    description = StringField()
    duration = IntField()


class UserCourseProgress(Document):
    user = ReferenceField(User)
    course = ReferenceField(Course)
    progress = DecimalField(min_value=0, max_value=100)