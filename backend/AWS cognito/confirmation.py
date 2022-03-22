import os
import boto3
from dotenv import load_dotenv
load_dotenv()

#use email
username = ''
#confirm code from email 
confirm_code = ''

# find region name list
client = boto3.client('cognito-idp', region_name =os.getenv('COGNITO_REGION_NAME'))
response = client.confirmation(
    clientID= os.getenv('COGNITO_USER_CLIENT_ID'),
    username = username,
    confirm_code = confirm_code
)
print(response)