import BlynkLib
import smbus
import time
#import socket
from BlynkLib import Blynk

# Define I2C bus and LIS3DH address
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1, for Raspberry Pi 3 or newer
lis3dh_addr = 0x19    # Default I2C address for LIS3DH

# Initialize LIS3DH
bus.write_byte_data(lis3dh_addr, 0x20, 0x27)  # Enable accelerometer in normal mode

# Blynk authentication token
#BLYNK_TEMPLATE_ID 'TMPL3L_j_mIV7'
#BLYNK_TEMPLATE_NAME 'LIS3DHwithRPI'
#define BLYNK_TEMPLATE_ID 'TMPL30XFtXCG1'
#define BLYNK_TEMPLATE_NAME "Quickstart Template"
#define BLYNK_AUTH_TOKEN "-Wb-QrMsfF84NHBHIwNiDSnStpsWHTU8"
#define WIFI_SSID "Terafac"
#define WIFI_PASS "Terafac@7078"
BLYNK_AUTH_TOKEN = 'V_ecG_eu1L94c1kmTsMJO9a6hz0myEBw'
 # Create a socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize Blynk with the specified server and port
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
	# sock.connect(('blynk.cloud', 443))
		# print("Connected to", host)
	#except Exception as e:
		#print("Connection failed:", str(e))
 

# Function for reading accelerometer data and sending it to the server
def read_accelerometer():
    data = bus.read_i2c_block_data(lis3dh_addr, 0x28 | 0x80, 6)
    x = data[0] | (data[1] << 8)
    y = data[2] | (data[3] << 8)
    z = data[4] | (data[5] << 8)

    print(f"X: {x}, Y: {y}, Z: {z}")

    # Send accelerometer values to virtual pins on the Blynk server
    blynk.virtual_write(0, x)  # Use virtual pin 0 for accelerometer X
    blynk.virtual_write(2, y)  # Use virtual pin 1 for accelerometer Y
    blynk.virtual_write(4, z)  # Use virtual pin 2 for accelerometer Z

    print("Accelerometer values sent to New Blynk Server!")

# Continuously run the Blynk application in a loop
while True:
    try:
        read_accelerometer()
        blynk.run()
        time.sleep(2)  # Adjust the sleep interval as needed
    except KeyboardInterrupt:
        break

