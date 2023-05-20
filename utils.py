import os
import pandas as pd
from twilio.rest import Client
from datetime import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


TWILIO_ACCOUNT_SID =os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN =os.environ["TWILIO_AUTH_TOKEN"]
PHONE_NUMBER ="+12545705477"


def request_api(api_key):

    url="https://api.bluelytics.com.ar/v2/latest"

    try :
        response = requests.get(url).json()
    except Exception as e:
        print(e)

    return response

def get_blue(response):

    timestamp = response["last_update"]
    parts = timestamp.split("T")
    fecha = parts[0]
    timep = parts[1].split(".") 
    hora = timep[0]

    compra = response["blue"]["value_buy"]
    venta = response["blue"]["value_sell"]
    prom = response["blue"]["value_avg"]

    return fecha, hora, compra, venta, prom

def create_df(data):

    col = ["Fecha", "Hora", "Compra", "Venta", "Prom"]
    df = pd.DataFrame([data],columns=col)

    return df

def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,input_date,df):

    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="\n Hola!  \n\n\n El valor del dolar al " + df["Fecha"][0] +" a las " + df["Hora"][0]  + " es: \n\n\n Compra: " + str(df["Compra"][0]) + " \n Venta: " + str(df["Venta"][0]) + "\n Valor promedio: " + str(df["Prom"][0]),
                        from_=PHONE_NUMBER,
                        to='+543512334798'
                    )

    return message.sid