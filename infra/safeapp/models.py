from django.db import models

# Create your models here.
from mongoengine import Document, IntField, StringField

from mongoengine import *
from datetime import datetime

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default="citizen")

class Report(Document):
    user_email = StringField()
    category = StringField()
    description = StringField()
    location = StringField()
    image = StringField()
    ai_result = StringField()
    status = StringField(default="Pending")
    created_at = DateTimeField(default=datetime.now)

class Compensation(Document):
    victim_email = StringField()
    report_id = StringField(required=True)
    ai_result = StringField()
    amount = FloatField(default=0)
    status = StringField(default="Pending")
    created_at = DateTimeField(default=datetime.utcnow)

class Notification(Document):

    message = StringField()

    is_read = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow)