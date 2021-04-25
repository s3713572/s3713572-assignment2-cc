import boto3
from music.models import Login
from boto3.dynamodb.conditions import Key, Attr


def is_login_match(email, password):
    login = Login.where(Attr('email').eq(email) & Attr('password').eq(password))
    if len(login)==0:
        return False
    return True

def is_login_exist(email):
    login = Login.find(email)
    if login:
        return True
    return False