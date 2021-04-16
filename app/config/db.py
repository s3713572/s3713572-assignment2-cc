import os
from dotenv import dotenv_values

config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ  # override loaded values with environment variables
}

db_conifg = {
  'MYSQL_HOST': config['MYSQL_HOST'],
  'MYSQL_USER': config['MYSQL_USER'],
  'MYSQL_PASSWORD': config['MYSQL_PASSWORD'],
  'MYSQL_DB': config['MYSQL_DB']
}