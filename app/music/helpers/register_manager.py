import boto3
from music.models import Login
from boto3.dynamodb.conditions import Key, Attr


def is_email_exist(email):
    login = Login.find(email)
    if login:
        return True
    return False

def create_item(email, user_name, password):
    login = Login(email, user_name, password)
    login.insert()