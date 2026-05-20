import paho.mqtt.client as mqtt
import csv
import json
import openpyxl
import os

HOST     = "da1370383cac40dea41673d21c76e2c6.s1.eu.hivemq.cloud"
PORT     = 8883
USERNAME = ""
PASSWORD = ""
TOPIC    = "fishing/boats"


EXCEL_FILE = "fishing_data.xlsx"
HEADERS = ["date", "time", "lat", "lng", "temp"]

# Create Excel file with headers if not exists
if not os.path.exists(EXCEL_FILE):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fishing Data"
    ws.append(HEADERS)
    wb.save(EXCEL_FILE)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected! Waiting for data...")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received: {payload}")
    
    data = json.loads(payload)
    
    # Open existing file and append row
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([data["date"], data["time"], data["lat"], data["lng"], data["temp"]])
    wb.save(EXCEL_FILE)
    
    print("Saved to Excel!")
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to HiveMQ...")
client.connect(HOST, PORT)
client.loop_forever()
