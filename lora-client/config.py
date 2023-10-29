import ubinascii
import machine

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MESSAGE_INTERVAL = 10
