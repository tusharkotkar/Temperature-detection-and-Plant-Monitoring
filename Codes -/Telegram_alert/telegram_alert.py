import requests               #for making HTTP requests
import json                   #Library for handling json data
import time                   #module for sleep operation

from boltiot import Bolt      #importing Bolt from boltiot module
import conf

mybolt = Bolt(conf.bolt_api_key, conf.device_id)

def get_sensor_value_from_pin(pin):
        """Returns the sensor value. Returns -999 if request fails"""
        try:
                response = mybolt.analogRead(pin)
                data = json.loads(response)
                if data["success"] != 1:
                   print("Request not successfull")
                   print("This is the response->", data)
                   return -999
                sensor_value = int(data["value"])
                return sensor_value
        except Exception as e:
                print("Something went wrong when returning the sensor value")
                print(e)
                return -999

def send_telegram_message(message):
    """Sends message via Telegram"""
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id": conf.telegram_chat_id,
        "text": message
    }
    try:
        response = requests.request(
            "POST",
            url,
            params=data
        )
        print("This is the Telegram URL")
        print(url)
        print("This is the Telegram response")
        print(response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False
while True:
        #Step 1
        sensor_value = get_sensor_value_from_pin("A0")
        print("The current sensor value is:", sensor_value)

        #step2
        if sensor_value == -999:
           print("Request was unsucessful.Skipping.")
           time.sleep(50)
           continue

        #step3
        if sensor_value >= conf.threshold:
           print("Sensor value has exceeded threshold")
           message = "Alert! Sensor valuehas exceeded "  + str(conf.threshold) + \
                ". The current value is " + str(sensor_value)
           telegram_status = send_telegram_message(message)
           print("This is the Telegram status:", telegram_status)

        #Step4
        time.sleep(50)
