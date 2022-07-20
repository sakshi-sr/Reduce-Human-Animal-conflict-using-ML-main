from twilio.rest import Client
import keys

client = Client(keys.account_sid,keys.auth_token)

message = client.messages.create(
    body="oye barbaad mutthal",
    from_=keys.twilio_number,
    to=keys.my_phone_number
)
print(message.body)