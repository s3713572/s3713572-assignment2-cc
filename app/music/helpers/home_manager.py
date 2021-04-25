import boto3
import threading
from music.models import Login, Music, Subscription
from boto3.dynamodb.conditions import Key, Attr
from queue import Queue
import uuid

def filt_music(title,artist,year,email):

    if title and artist and year:
        musics = Music.where(Attr('title').eq(title)&Attr('artist').eq(artist)&Attr('year').eq(year))
    if title and artist and not year:
        musics = Music.where(Attr('title').eq(title)&Attr('artist').eq(artist))
    elif title and not artist and not year:
        musics = Music.where(Attr('title').eq(title))
    elif not title and artist and not year:
        musics = Music.where(Attr('artist').eq(artist))
    elif not title and not artist and year:
        musics = Music.where(Attr('year').eq(year))
    elif not title and artist and year:
        musics = Music.where(Attr('artist').eq(artist)&Attr('year').eq(year))
    else:
        musics = Music.all()
    q = Queue()
    threads = []
    fetched_musics = []
    for music in musics:
        thread = threading.Thread(target=single_music,args=(music,email,q))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    for _ in range(len(threads)):
        fetched_musics.append(q.get())

    return fetched_musics


def fetch_musics(email):
    q = Queue()
    musics = Music.all()
    threads = []
    fetched_musics = []
    for music in musics:
        thread = threading.Thread(target=single_music,args=(music,email,q))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    for _ in range(len(threads)):
        fetched_musics.append(q.get())

    return fetched_musics
    

def single_music(music, email, q):

    img_url = "https://music-image.s3.amazonaws.com/" + music.music_id
    if is_music_subscripted(music.music_id, email):
        button_status = "Subscripted"
    else:
        button_status = "Subscript"
    result = MusicsHelper(music.title,music.artist,music.year,music.web_url,img_url,music.music_id,button_status)
    q.put(result)

        

def is_music_subscripted(music_id,email):
    if Subscription.where(Attr("email").eq(email)&Attr("music_id").eq(music_id)):
        return True
    return False

def onlick_subscription_button(button_value, music_id, email):
    if button_value == "Subscript":
        subscription_id = str(uuid.uuid1()).replace("-","")

        subscription = Subscription(music_id, email, subscription_id)
        subscription.insert()
        return "Subscript"
    if button_value == "Subscripted":
        subscriptions = Subscription.where(Attr("email").eq(email)&Attr("music_id").eq(music_id))
        for subscription in subscriptions:
            subscription_id = subscription.subscription_id
            Subscription.delete(subscription_id)
        return "de-Subscript"


class MusicsHelper():
    def __init__(self, title, artist, year, web_url, img_url, music_id, button_status):
        self.music_id = music_id
        self.title = title
        self.artist = artist
        self.year = year
        self.web_url = web_url
        self.img_url = img_url
        self.music_id = music_id
        self.button_status = button_status

