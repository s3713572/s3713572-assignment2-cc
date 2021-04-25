import boto3
from music import dynamodb
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import uuid

class NoPrimaryKeyError(Exception):
    pass


class DynamoModel():
    primary_key = None
    def __init__(self):
        self.table_name = self.__class__.__name__
        if self.primary_key == None:
            raise NoPrimaryKeyError("The primary key is not defined")
        

    def insert(self):
        table = dynamodb.Table(self.table_name)
        table.put_item(
            Item=self.props()
        )
    
    def props(self):   
        table_dict = self.__dict__
        del table_dict['table_name']
        return table_dict

    # Find the object by its primary key
    # @params dict key
    # @return DynamoModel
    @classmethod
    def find(self, value):
        try:
            table = dynamodb.Table(self.__name__)
            response = table.get_item(
                Key={self.primary_key: value}
            )
            item = response['Item']
            return self(**item)
        except ClientError as e:
            return None
        except KeyError:
            return None
        

    @classmethod
    def where(self, querys):
        try:
            table = dynamodb.Table(self.__name__)
            response = table.scan(
                FilterExpression = querys
            )
            items = response['Items']
            return list(map(lambda item: self(**item), items))
        except ClientError as e:
            return None   
        except KeyError:
            return None

    @classmethod
    def delete(self, value):
        table = dynamodb.Table(self.__name__)
        table.delete_item(
            Key={self.primary_key: value}
        )
    
    @classmethod
    def all(self):
        table = dynamodb.Table(self.__name__)
        response = table.scan()
        datas = response['Items']

        while 'LastEvaluateKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            datas.extend(response['Items'])
        
        models = []
        for data in datas:
            models.append(self(**data))     
        return models


class Login(DynamoModel):
    primary_key = "email"
    def __init__(self, email, user_name, password):
        super().__init__()
        self.email = email
        self.user_name = user_name
        self.password = password

class Music(DynamoModel):
    primary_key="music_id"
    def __init__(self, title, artist, year, web_url, img_url, music_id=None):
        super().__init__()
        self.music_id = music_id
        self.title = title
        self.artist = artist
        self.year = year
        self.web_url = web_url
        self.img_url = img_url

class Subscription(DynamoModel):
    primary_key="subscription_id"
    def __init__(self, music_id, email, subscription_id=None):
        super().__init__()
        self.music_id = music_id
        self.email = email
        self.subscription_id = subscription_id

class Queue(object):
    def __init__(self):
        self.item = []
    
    def __repr__(self):
        return "{}".format(self.item)

    def __str__(self):
        return "{}".format(self.item)

    def enque(self, add):
        self.item.insert(0,add)
        return True
    
    def size(self):
        return len(self.item)

    def isempty(self):
        if self.size() == 0:
            return True
        else:
            return False

    def deque(self):
        if self.size() == 0:
            return None
        else:
            return self.item.pop()



