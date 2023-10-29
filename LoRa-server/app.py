import time
from raspi_lora import LoRa, ModemConfig
import struct

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

    unpacked_data = struct.unpack('12sfff', payload.message)
    client_id, temperature, humidity, pressure = unpacked_data

    print("client:", client_id)
    print("temperature:", temperature)
    print("humidity:", humidity)
    print("pressure", pressure)
    print("------------------------")

# Use chip select 0. GPIO pin 17 will be used for interrupts
# The address of this device will be set to 2
lora = LoRa(0, 17, 2, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=20, acks=True, freq=868)
lora.on_recv = on_recv

lora.set_mode_rx()

while True:
    time.sleep(0.1)
