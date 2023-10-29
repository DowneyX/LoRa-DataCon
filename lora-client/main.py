from machine import Pin, SoftI2C
from time import sleep
from ulora import LoRa, ModemConfig, SPIConfig
import BME280
import config
import struct

# Lora Parameters
RFM95_RST = 18
RFM95_SPIBUS = SPIConfig.esp32_1
RFM95_CS = 5
RFM95_INT = 19
RF95_FREQ = 868.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2


def getData():
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)

    bme = BME280.BME280(i2c=i2c)

    client_id = config.CLIENT_ID  # Encode the client ID as bytes
    temperature = float(bme.temperature)
    humidity = float(bme.humidity)
    pressure = float(bme.pressure)
    
    data_bytes = struct.pack('fff', temperature, humidity, pressure)

    return client_id + data_bytes

 
# initialise radio
lora = LoRa(RFM95_SPIBUS, RFM95_INT, CLIENT_ADDRESS, RFM95_CS,
            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)


# loop and send data
while True:
    data = getData()
    lora.send_to_wait(data, SERVER_ADDRESS)
    print(f"send {data}")
    sleep(config.MESSAGE_INTERVAL)
