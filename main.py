import asyncio
from bleak import BleakScanner, BleakClient
import requests

URL = "http://localhost:8080"

async def handle_command(command):
    try:
        response = requests.post(URL, json={"command": command})
        print(f"HTTP Request sent. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send HTTP request: {e}")

async def notification_handler(sender, data):
    command = data.decode('utf-8').strip()
    print(f"Received command: {command}")
    await handle_command(command)

async def connect_and_listen():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()

    if not devices:
        print("No devices found.")
        return

    for idx, device in enumerate(devices):
        print(f"[{idx}] Device: {device.name} | Address: {device.address}")

    for device in devices:
        try:
            print(f"Connecting to {device.name} ({device.address})...")
            async with BleakClient(device.address) as client:
                print(f"Connected to {device.name} ({device.address})")

                # Assuming the device has a characteristic that notifies data
                # You may need to specify the correct UUID for your device
                characteristic_uuid = "your-characteristic-uuid"
                await client.start_notify(characteristic_uuid, notification_handler)

                print("Listening for commands...")
                await asyncio.sleep(60)  # Listen for 60 seconds
                await client.stop_notify(characteristic_uuid)

        except Exception as e:
            print(f"Failed to connect to {device.name} ({device.address}): {e}")

if __name__ == "__main__":
    asyncio.run(connect_and_listen())
