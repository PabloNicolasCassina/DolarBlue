import os
from twilio.rest import Client
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from utils import request_api, get_blue, create_df, send_message



TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
PHONE_NUMBER = "+12545705477"

input_date = datetime.now().strftime("%Y-%m-%d")
response = request_api("https://api.bluelytics.com.ar/v2/latest")
data = get_blue(response)
df = create_df(data)

# Send Message
message_id = send_message(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, input_date, df)

print('Mensaje Enviado con éxito ' + message_id)
