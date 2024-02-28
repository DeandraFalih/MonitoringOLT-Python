import minimalmodbus
import serial
import requests
import time
from contextlib import closing
import board
import adafruit_dht
import threading

# Konfigurasi Raspberry Pi GPIO untuk DHT22
DHT_SENSOR = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Konfigurasi PZEM-017
DEVICE_ADDRESS = 0x01
BAUD_RATE = 9600
TIMEOUT = 1
PORT = '/dev/ttyUSB0'

# Konfigurasi API endpoint
API_ENDPOINT = 'https://chyoad.cloud/api/sensor/create/236263-4DB7F8-754B9C?apiKey=3MHpKi-6AdMa7-953wQK-OBU3t8'

def read_dht22_data():
    try:
        temperature_c = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        return {
            'temperature_c': temperature_c,
            'humidity': humidity
        }
    except RuntimeError as error:
        print(error.args[0])
        return None

def read_pzem_data():
    try:
        with closing(serial.Serial(PORT, BAUD_RATE, timeout=TIMEOUT)) as ser:
            instrument = minimalmodbus.Instrument(ser, DEVICE_ADDRESS)
            voltage = instrument.read_float(0x0000, functioncode=4)
            current = instrument.read_float(0x0002, functioncode=4)
            power = instrument.read_float(0x0006, functioncode=4)
            energy = instrument.read_float(0x0008, functioncode=4)

            return {
                'voltage': voltage,
                'current': current,
                'power': power,
                'energy': energy
            }
    except minimalmodbus.IllegalRequestError as e:
        print(f"Error: {e}")
        return None

def send_data_to_api(data):
    try:
        response = requests.post(API_ENDPOINT, json=data)
        if response.status_code == 200:
            print("Data berhasil dikirim ke API")
        else:
            print("Gagal mengirim data ke API. Kode status:", response.status_code)
    except Exception as e:
        print("Terjadi kesalahan saat mengirim data ke API:", str(e))

def read_and_send_data():
    while True:
        dht_data = read_dht22_data()
        pzem_data = read_pzem_data()

        if dht_data and pzem_data:
            combined_data = {
                'tegangan': pzem_data['voltage'],
                'arus': pzem_data['current'],
                'daya': pzem_data['power'],
                'energi': pzem_data['energy'],
                'suhu': dht_data['temperature_c'],
                'kelembapan': dht_data['humidity']
            }
            send_data_to_api(combined_data)

        time.sleep(1)  # Membaca dan mengirim data setiap detik

if _name_ == "_main_":
    # Jalankan fungsi pembacaan dan pengiriman data dalam thread terpisah
    data_thread = threading.Thread(target=read_and_send_data)
    data_thread.start()

    try:
        # Tunggu hingga thread selesai (dalam hal ini tidak pernah selesai karena loop tak terbatas)
        data_thread.join()
    except KeyboardInterrupt:
        print("Pembacaan data dihentikan.")