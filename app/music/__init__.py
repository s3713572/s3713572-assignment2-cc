import boto3
from flask import Flask
from dotenv import dotenv_values
from config.db import db_conifg


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5f1306a3a5db43729df8b941f38c692'
dynamodb = boto3.resource('dynamodb',aws_access_key_id='AKIAQFULF3NXYNWPGSPQ', aws_secret_access_key='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', region_name='us-east-1')
s3 = boto3.resource('s3',aws_access_key_id='AKIAQFULF3NXYNWPGSPQ', aws_secret_access_key='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', region_name='us-east-1')



from music import routes