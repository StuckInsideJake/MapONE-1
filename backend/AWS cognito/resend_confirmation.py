import os
import boto3
from dotenv import load_dotenv
load_dotenv()

#use email
# later use database user id email 
username = ''

# find region name list 
# lateron find if there is a library to use for this 
client = boto3.client('cognito-idp', region_name =os.getenv('COGNITO_REGION_NAME'))
# sends confirmation email with code to verify said user email in userpool
response = client.resend_confirmation(
    clientID= os.getenv('COGNITO_USER_CLIENT_ID'),
    username = username
)
print(response)