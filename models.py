import boto3
import os
from dotenv import load_dotenv
from boto3.dynamodb.conditions import Key
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

class User:
    def __init__(self, table):
        self.table = table

    def create_table(self):
        existing_tables = dynamodb.meta.client.list_tables()['TableNames']
        if 'UserData' not in existing_tables:
            table = dynamodb.create_table(
                TableName='UserData',
                KeySchema=[
                    {
                        'AttributeName': 'username',
                        'KeyType': 'HASH' 
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'username',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName='UserData')
            self.table = table
        else:
            self.table = dynamodb.Table('UserData')

    def put_user(self, username, password):
        password_hash = generate_password_hash(password)
        self.table.put_item(
            Item={
                'username': username,
                'password_hash': password_hash
            }
        )

    def get_user(self, username):
        response = self.table.get_item(
            Key={
                'username': username
            }
        )
        return response.get('Item')

    def check_password(self, user, password):
        if user and 'password_hash' in user:
            return check_password_hash(user['password_hash'], password)
        return False

class Message:
    def __init__(self, table):
        self.table = table

    def create_table(self):
        existing_tables = dynamodb.meta.client.list_tables()['TableNames']
        if 'ChatData' not in existing_tables:
            table = dynamodb.create_table(
                TableName='ChatData',
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'N'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.meta.client.get_waiter('table_exists').wait(TableName='ChatData')
            self.table = table
        else:
            self.table = dynamodb.Table('ChatData')

    def put_message(self, sender, content):
        timestamp = datetime.now().strftime("%H:%M")
        self.table.put_item(
            Item={
                'id': int(timestamp.replace(":", "")),
                'sender': sender,
                'content': content,
                'timestamp': timestamp
            }
        )

    def get_messages(self):
        response = self.table.scan()
        return response.get('Items')

def create_tables(app):
    # Create User table
    user_table = dynamodb.Table('UserData')
    user = User(user_table)
    user.create_table()

    # Create Message table
    message_table = dynamodb.Table('ChatData')
    message = Message(message_table)
    message.create_table()