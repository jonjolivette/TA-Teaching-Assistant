import datetime
import time
from peewee import *
import moment

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('ta.db')


class User(UserMixin, Model):
    username = CharField()
    email = CharField(unique=True)
    role = CharField()
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    course = CharField()
    image_file = BlobField(default="default.png")
    event_assigned = BooleanField(default=False)

    class Meta:
        database = DATABASE

    def get_events(self):
        return Event.select().where(Event.user == self)

    @classmethod
    def create_user(cls, username, email, role, password, event_assigned=False, image_file="default.png", course="General"):
        try:
            cls.create(
                username=username,
                email=email,
                role=role,
                event_assigned=event_assigned,
                password=generate_password_hash(password),
                course=course,
                image_file=image_file
            )
        except IntegrityError:
            raise ValueError("User already exists")


class Event(Model):
    student = ForeignKeyField(
    model=User,
    backref='events',
    null=True
    )
    instructor = ForeignKeyField(
    model=User,
    backref='events'
    )
    date = DateField(default=moment.utcnow())
    time = TimeField(default=datetime.time(14,0,0))
    duration = CharField(default="15")
    notes = CharField(max_length=256, default="Bleep Bloop")

    class Meta:
        database = DATABASE

    @classmethod
    def create_event(cls, instructor, date, time):
        try:
            cls.create(
                instructor=instructor,
                date=date,
                time=time
            )
        except IntegrityError:
            raise

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Event], safe=True)
    DATABASE.close()

