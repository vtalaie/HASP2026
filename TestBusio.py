import board
import busio
import time

# Initialize the I2C bus
#i2c = busio.I2C(board.SCL, board.SDA)
i2c = busio.I2C(3, 2)

# Device address (replace with your device's address, e.g., 0x18 for a temp sensor)
DEVICE_ADDRESS = 0x2C

while not i2c.try_lock():
    pass

try:
    # --- Writing bytes ---
    # To write a single byte (e.g., a register address 0x05)
    # The data must be in a bytes object or bytearray
    register_address = bytes([0x01])
    #i2c.writeto(DEVICE_ADDRESS, register_address, stop=False) # Keep the bus locked for a combined transaction
    i2c.writeto(DEVICE_ADDRESS, register_address) # Keep the bus locked for a combined transaction

    # --- Reading bytes ---
    # Create a bytearray buffer to store the incoming data
    # The buffer size determines how many bytes are read (e.g., 2 bytes)
    result_buffer = bytearray(32)
    i2c.readfrom_into(DEVICE_ADDRESS, result_buffer)

    print(f"Read bytes: {result_buffer}")

finally:
    # Always unlock the bus when done
    i2c.unlock()
