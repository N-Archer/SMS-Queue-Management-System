import os
from twilio.rest import Client

def send_sms(body="somebody", to=""):
    # Your Account SID from twilio.com/console
    account_sid = os.environ["twilio_sid"]
    # Your Auth Token from twilio.com/console
    auth_token  = os.environ["twilio_auth_token"]
    dest_phone_num = os.environ["personal_num"]
    twilio_num = os.environ["twilio_phone_num"]

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=dest_phone_num, 
        from_=twilio_num,
        body=body)

    print(message.sid)