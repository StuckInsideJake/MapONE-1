#sign-up 
import os
import boto3
from dotenv import load_dotenv
load_dotenv()

# Note #
#----------------------------------------------------------------------#
# Currently the aws server set up seems to not want to work
# it wishes for a creditcard to be inputted before creation of 
# a server can happen. Due to this I wish not to put my 
# personal credit card on this especially since we will
# be handing it off to our clients after the semseter is over
# I also am unsure how much the free version would allow for uses and 
# run time before the credit card would be charged.
#---------------------------------------------------------------------#

#use  any email for testing.
# later on set up to search for user email in database  
username = ''
# give a password for setting up user pool user
# later on check for user password from database?
password = ''
# find region name list online for the region of the world user may be in. 
# possible library to automate it or find it for us
client = boto3.client('cognito-idp', region_name =os.getenv('COGNITO_REGION_NAME'))
#sets up user in user pool 
response = client.sign_up(
    clientID= os.getenv('COGNITO_USER_CLIENT_ID'),
    username = username
    password = password
)
print(response)
