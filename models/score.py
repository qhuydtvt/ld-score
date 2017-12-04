from mongoengine import *


class Score(Document):
    name = StringField(max_length=30)
    score = IntField()
    added_time = DateTimeField()