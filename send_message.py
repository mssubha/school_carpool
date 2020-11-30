
import os
from twilio.rest import Client

def send_message (phone_number, message):

    account_sid = os.environ['twilio_sid'] 
    auth_token = os.environ['twilio_api']  
    twilio_phone = os.environ['twilio_phone'] 

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=twilio_phone,
        body= message,
        to=phone_number 
    )

    print(message.sid)