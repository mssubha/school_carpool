
import os
from twilio.rest import Client

account_sid = os.environ['twilio_sid'] 
auth_token = os.environ['twilio_api']  

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='+12058273855',
    body= 'Hi from Subha Twilio',
    to='+14152509456'
)

print(message.sid)