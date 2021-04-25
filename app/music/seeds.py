from music import app, dynamodb, s3
from music.models import Login, Music
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
import requests
import uuid


# from music.helpers.seeddata_manager import is_seed_data_exist
def create_subscription_table():
    return False

def create_music_table():
    try:
        table = dynamodb.create_table(
        TableName='Music',
        KeySchema=[
            {
                'AttributeName': 'music_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'music_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='Music')
    except ClientError as e:
        return

def load_json_data(musics):
    music = Music.where(Attr('title').eq('Watching the Wheels')&Attr('artist').eq('John Lennon')&Attr('img_url').eq('http://www.songnotes.cc/images/artists/JohnLennon.jpg')&Attr('web_url').eq('http://www.songnotes.cc/songs/5-john-lennon-watching-the-wheels'))
    if len(music) == 1:
        return
    table = dynamodb.Table('Music')
    for music in musics['songs']:

        title = music['title']
        artist = music['artist']
        try:
            year = music['year']
        except ValueError:
            year = None
        web_url = music['web_url']
        try:
            img_url = music['img_url']
        except ValueError:
            img_url = None
        
        music_id = str(uuid.uuid1()).replace("-","")
        item = Music(title,artist,year,web_url,img_url, music_id)
        item.insert()

        bucket_name = "music-image"
        internet_img_url = img_url
        req_for_image = requests.get(internet_img_url, stream=True)
        file_object_from_req = req_for_image.raw
        req_data = file_object_from_req.read()


        s3.Bucket(bucket_name).put_object(Key= item.music_id, Body=req_data)

def create_10_logins():
    if Login.find('s37135720'):
        return
    
    table = dynamodb.Table('Login')
    table.put_item(
    Item={
            'email': 's37135720',
            'user_name': 'Qucheng Zhang 0',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135721',
            'user_name': 'Qucheng Zhang 1',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135722',
            'user_name': 'Qucheng Zhang 2',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135723',
            'user_name': 'Qucheng Zhang 3',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135724',
            'user_name': 'Qucheng Zhang 4',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135725',
            'user_name': 'Qucheng Zhang 5',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135726',
            'user_name': 'Qucheng Zhang 6',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135727',
            'user_name': 'Qucheng Zhang 7',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135728',
            'user_name': 'Qucheng Zhang 8',
            'password': '012345',
        }
    )
    table.put_item(
    Item={
            'email': 's37135729',
            'user_name': 'Qucheng Zhang 9',
            'password': '012345',
        }
    )
    




