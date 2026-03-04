from mongoengine import Document, StringField, BooleanField, EmailField, ListField, URLField, DecimalField, ReferenceField, DateTimeField, IntField
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)
    skills = ListField(StringField())
    portfolio = URLField()
    courses_completed = ListField(StringField())
    reviews = ListField(StringField())
    is_mentor = BooleanField(default=False)
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

class Application(Document):
    user = ReferenceField(User)
    job = ReferenceField(JobPost)
    applied_at = DateTimeField()

class Course(Document):
    title = StringField(required=True)
    description = StringField()
    duration = IntField()

class UserCourseProgress(Document):
    user = ReferenceField(User)
    course = ReferenceField(Course)
    progress = DecimalField(min_value=0, max_value=100)

    # Defining UserCourseProgress model
class UserCourseProgress(Document):
    user = ReferenceField(User)
    course = ReferenceField(Course)
    progress = DecimalField(min_value=0, max_value=100)

# Creating Application model
class Application(Document):
    user = ReferenceField(User)
    job = ReferenceField(JobPost)
    applied_at = DateTimeField(default=datetime.utcnow)