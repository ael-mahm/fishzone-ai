import json
import time
import serial
from supabase import create_client, Client

# ── Supabase settings ──────────────────────────────────────────
SUPABASE_URL = "https://qyfaucvzmzkmkzevgdoq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5ZmF1Y3Z6bXprbWt6ZXZnZG9xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAxNzIyMzcsImV4cCI6MjA5NTc0ODIzN30.dYH4y2UFD42xxg1OHfJ1HGfP-9LNsD0jVNW4LwNVPQ0"                       # ← Project API key

# ── Serial settings ────────────────────────────────────────────
SERIAL_PORT = "COM11"
BAUD_RATE   = 9600

# ── Setup ──────────────────────────────────────────────────────
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ Connected to Supabase!")

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
print(f"✅ Listening on {SERIAL_PORT}...")

# ── Main loop ──────────────────────────────────────────────────
while True:
    line = ser.readline().decode("utf-8").strip()

    if line.startswith("{"):
        print(f"📥 From Proteus: {line}")

        try:
            data = json.loads(line)

            # Map JSON fields → table columns
            record = {
                "boat_name": data.get("boat_name"),
                "latitude":  data.get("lat"),
                "longitude": data.get("lng"),
                "sst":       data.get("temp"),
                "presence":  data.get("presence"),
                "trip_time": data.get("time"),
                "trip_date": data.get("date"),
            }

            response = supabase.table("fishing_trips").insert(record).execute()
            print(f"✅ Inserted: {record}")

        except json.JSONDecodeError:
            print(f"❌ Invalid JSON: {line}")
        except Exception as e:
            print(f"❌ Supabase error: {e}")