import minimalmodbus
import serial
import time
from contextlib import closing
import time
import requests
# import Adafruit_DHT

# Define your WiFi SSID and password

# GPIO pin for DHT sensor (change as needed)
# DHT_PIN = 4
DEVICE_ADDRESS = 0x01
BAUD_RATE = 9600
TIMEOUT = 1
PORT = '/dev/ttyUSB0'

# dhtDevice = Adafruit_DHT.DHT22(board.D18)
API_KEY = ""
URL = "https://srv-olt.iotanic.id/api/sensor/create/1/:apikey"

interval = 20 #detik
SensorTime = 0
TsTime = 0
# Raspberry Pi needs to be connected to the internet
# for HTTP requests to work

def connect_wifi():
    import subprocess
    cmd = f"sudo iwlist wlan0 scan | grep ESSID | grep '{ssid}'"
    while True:
        output = subprocess.check_output(cmd, shell=True)
        if ssid.encode() in output:
            print("Connecting to WiFi...")
            subprocess.check_output(f"sudo wpa_passphrase {ssid} {password} >> /etc/wpa_supplicant/wpa_supplicant.conf", shell=True)
            subprocess.check_output("sudo ifdown wlan0 && sudo ifup wlan0", shell=True)
            print("Connected")
            break
        time.sleep(5)

#ORIGINAL (WIRA)
# def send_data(temperature, humidity, max_voltage):
#     url = "http://srv-olt.iotanic.id/api/sensor/create/1/:apikey"
#     headers = {"Content-Type": "application/x-www-form-urlencoded"}
#     data = f"temperature={temperature:.1f}&humidity={humidity:.1f}&tegangan={max_voltage:.1f}"
#     response = requests.post(url, data=data, headers=headers)
#     print("HTTP Response Code:", response.status_code)

#MOD
def send_data(voltage, current, power, energy):
    url = "http://srv-olt.iotanic.id/api/sensor/create/1/:apikey"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"voltage={voltage:.1f}&current={current:.1f}&power={power:.1f}&energy={energy:.1f}"
    response = requests.post(url, data=data, headers=headers)
    print("HTTP Response Code:", response.status_code)


# def read_pzem_data():
#     # Initialize the connection to the PZEM device
#     connect_wifi()
#     #max_voltage = 0.0
#     start_time = time.time()
#     current_time = start_time
#     instrument = minimalmodbus.Instrument(PORT, DEVICE_ADDRESS)
#     instrument.serial.baudrate = 9600
#     instrument.serial.bytesize = 8
#     instrument.serial.parity = serial.PARITY_NONE
#     instrument.serial.stopbits = 2
#     instrument.serial.timeout = 1
    
    #ORIGINAL (GITHUB)
    # try:
    #     # Read measurement data
    #     voltage = instrument.read_register(0x0000, number_of_decimals=2, functioncode=4)
    #     current = instrument.read_register(0x0001, number_of_decimals=2, functioncode=4)
    #     power_low = instrument.read_register(0x0002, functioncode=4)
    #     power_high = instrument.read_register(0x0003, functioncode=4)
    #     power = (power_high << 16) + power_low
    #     energy_low = instrument.read_register(0x0004, functioncode=4)
    #     energy_high = instrument.read_register(0x0005, functioncode=4)
    #     energy = (energy_high << 16) + energy_low
        
    #     # Read alarm status
    #     high_voltage_alarm = instrument.read_register(0x0006, functioncode=4)
    #     low_voltage_alarm = instrument.read_register(0x0007, functioncode=4)

    #     print(f"Voltage: {voltage} V")
    #     print(f"Current: {current} A")
    #     print(f"Power: {power * 0.1} W")
    #     print(f"Energy: {energy} Wh")
        
    #     # Print alarm statuses
    #     print(f"High Voltage Alarm: {'Alarm' if high_voltage_alarm == 0xFFFF else 'Clear'}")
    #     print(f"Low Voltage Alarm: {'Alarm' if low_voltage_alarm == 0xFFFF else 'Clear'}")
        
    # except minimalmodbus.IllegalRequestError as e:
    #     print(f"Error: {e}")

    # finally:
    #     time.sleep(1)
    #     instrument.serial.close()

    # MOD
#     while current_time - start_time < 10:
#         # Read measurement data
#         voltage = instrument.read_register(0x0000, number_of_decimals=2, functioncode=4)
#         current = instrument.read_register(0x0001, number_of_decimals=2, functioncode=4)
#         power_low = instrument.read_register(0x0002, functioncode=4)
#         power_high = instrument.read_register(0x0003, functioncode=4)
#         power = (power_high << 16) + power_low
#         energy_low = instrument.read_register(0x0004, functioncode=4)
#         energy_high = instrument.read_register(0x0005, functioncode=4)
#         energy = (energy_high << 16) + energy_low
        
#         # Read alarm status
#         high_voltage_alarm = instrument.read_register(0x0006, functioncode=4)
#         low_voltage_alarm = instrument.read_register(0x0007, functioncode=4)

#         print(f"Voltage: {voltage} V")
#         print(f"Current: {current} A")
#         print(f"Power: {power * 0.1} W")
#         print(f"Energy: {energy} Wh")
#         # Print alarm statuses
#         print(f"High Voltage Alarm: {'Alarm' if high_voltage_alarm == 0xFFFF else 'Clear'}")
#         print(f"Low Voltage Alarm: {'Alarm' if low_voltage_alarm == 0xFFFF else 'Clear'}")

#         current_time = time.time()
#         time.sleep(1)
        
#     if minimalmodbus.IllegalRequestError as e:
#             print(f"Error: {e}")

#     time.sleep(1)
#     instrument.serial.close()

# if __name__ == "__main__":
#     read_pzem_data()

def read_pzem_data():
    # Initialize the connection to the PZEM device
    connect_wifi()
    start_time = time.time()
    current_time = start_time
    instrument = minimalmodbus.Instrument(PORT, DEVICE_ADDRESS)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 2
    instrument.serial.timeout = 1

    retry_count = 0
    max_retries = 3  # Adjust the number of retries as needed

    while current_time - start_time < 10:
        try:
            # Read measurement data
            voltage = instrument.read_register(0x0000, number_of_decimals=2, functioncode=4)
            current = instrument.read_register(0x0001, number_of_decimals=2, functioncode=4)
            power_low = instrument.read_register(0x0002, functioncode=4)
            power_high = instrument.read_register(0x0003, functioncode=4)
            power = (power_high << 16) + power_low
            energy_low = instrument.read_register(0x0004, functioncode=4)
            energy_high = instrument.read_register(0x0005, functioncode=4)
            energy = (energy_high << 16) + energy_low

            # Read alarm status
            high_voltage_alarm = instrument.read_register(0x0006, functioncode=4)
            low_voltage_alarm = instrument.read_register(0x0007, functioncode=4)

            print(f"Voltage: {voltage} V")
            print(f"Current: {current} A")
            print(f"Power: {power * 0.1} W")
            print(f"Energy: {energy} Wh")
            # Print alarm statuses
            print(f"High Voltage Alarm: {'Alarm' if high_voltage_alarm == 0xFFFF else 'Clear'}")
            print(f"Low Voltage Alarm: {'Alarm' if low_voltage_alarm == 0xFFFF else 'Clear'}")

            current_time = time.time()
            time.sleep(1)

        except minimalmodbus.IllegalRequestError as e:
            print(f"Error: {e}")
            retry_count += 1
            if retry_count >= max_retries:
                print(f"Max retries ({max_retries}) reached. Exiting loop.")
                break
            else:
                print(f"Retrying... (Attempt {retry_count}/{max_retries})")
                time.sleep(1)  # Add a short delay before retrying

    time.sleep(1)
    instrument.serial.close()

if __name__ == "__main__":
    read_pzem_data()