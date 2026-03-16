from mongoengine import Document, StringField, BooleanField, EmailField, ListField, URLField, DecimalField, ReferenceField, DateTimeField, IntField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import connect.db

class User(UserMixin, Document):
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    is_admin = db.BooleanField(default=False)

    skills = db.ListField(StringField())
    portfolio = db.URLField()
    courses_completed = db.ListField(StringField())
    reviews = db.ListField(StringField())

    is_mentor = Bdb.ooleanField(default=False)
    mentor_bio = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class JobPost(db.Document):
    title = db.StringField(required=True)
    company = db.StringField(required=True)
    location = db.StringField(required=True)
    category = db.StringField(required=True)
    description = db.StringField()
    salary = db.DecimalField()
    employer = db.ReferenceField(User)


class Application(Document):
    user = ReferenceField(User)
    job = ReferenceField(JobPost)
    applied_at = DateTimeField(default=datetime.utcnow)


class Course(Document):
    title = StringField(required=True)
    description = StringField()
    duration = IntField()


class UserCourseProgress(Document):
    user = ReferenceField(User)
    course = ReferenceField(Course)
    progress = DecimalField(min_value=0, max_value=100)