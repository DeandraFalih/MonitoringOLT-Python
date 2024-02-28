import requests
import RPi.GPIO as GPIO
import time

# Replace with your actual API endpoint
RELAY_API_ENDPOINT = 'https://chyoad.cloud/api/relay/236263-4DB7F8-754B9C?apiKey=3MHpKi-6AdMa7-953wQK-OBU3t8'

# Replace with the actual GPIO pin number you're using for the relay
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

def fetch_relay_status(api_endpoint):
    try:
        response = requests.get(api_endpoint)
        if response.status_code == 200:
            relay_status = response.json().get('status', 0)
            return relay_status
        else:
            print("Failed to fetch relay status from API. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching relay status from API:", str(e))
        return None

def control_relay(status):
    if status == 1:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn relay on
        print("Relay On")
    else:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn relay off
        print("Relay Off")

if __name__ == "__main__":
    try:
        while True:
            # Fetch relay status from the API
            relay_status = fetch_relay_status(RELAY_API_ENDPOINT)

            if relay_status is not None:
                # Control the relay based on the received status
                control_relay(relay_status)

            # Wait for some time before fetching status again
            time.sleep(5)

    except KeyboardInterrupt:
        print("Script terminated by user.")
        GPIO.cleanup()  # Cleanup GPIO settings on keyboard interrupt
