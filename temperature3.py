import BlynkLib
import board
import busio
import adafruit_sht4x
import time
from BlynkTimer import BlynkTimer

BLYNK_AUTH_TOKEN = 'V_ecG_eu1L94c1kmTsMJO9a6hz0myEBw'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
print("Token validated successfully")

# Initialize the I2C bus and SHT4x sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht4x.SHT4x(i2c)
print("Sensor initialized")

# Create a timer to read and send sensor data every 10 seconds (adjust as needed)
timer = BlynkTimer()

# Function to read sensor data and send it to Blynk
def read_and_send_sensor_data():
    try:
        # Read sensor data
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        print(f"Temperature: {temperature} °C, Humidity: {humidity} %RH")

        # Send data to Blynk virtual pins
        blynk.virtual_write(2, temperature)  # Virtual Pin V2 for temperature
        blynk.virtual_write(3, humidity)     # Virtual Pin V3 for humidity

    except Exception as e:
        print(f"Error reading sensor data: {str(e)}")

# Function to sync the data from virtual pins
@blynk.on("connected")
def blynk_connected():
    print("Raspberry Pi Connected to New Blynk")
    # Start the timer when connected
    timer.set_interval(10, read_and_send_sensor_data)

# Run the Blynk client
while True:
    read_and_send_sensor_data()
    blynk.run()
    timer.run()
    time.sleep(2)
