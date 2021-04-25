import boto3
from music.models import Login, Subscription, Music
from boto3.dynamodb.conditions import Key, Attr
from queue import Queue
import threading
from music.helpers.home_manager import single_music

def remove_music(music_id,email):
    subscriptions = Subscription.where(Attr('music_id').eq(music_id)&Attr('email').eq(email))
    for subscription in subscriptions:
        subscription.delete(subscription.subscription_id)
    