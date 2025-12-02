from smbus import SMBus
import time
from gpiozero import LED
from time import sleep

led = LED(17)

i2cbus = SMBus(1)

i2caddress = 0x1C
i2caddress_1 = 0x2A
i2caddress_2 = 0x2B

led.on()

# Reset
data = 0x02
i2cbus.write_byte_data(i2caddress, 0x04, data)
print(f"RSTR (Write): {hex(data)}")
data = 0x0A
i2cbus.write_byte_data(i2caddress, 0x04, data)
print(f"RSTR (Write): {hex(data)}")
data = 0x04
i2cbus.write_byte_data(i2caddress, 0x04, data)
print(f"RSTR (Write): {hex(data)}")
sleep(1)

# Who am I
data = i2cbus.read_byte_data(i2caddress, 0x00)
print(f"WHO_AM_I (Read): {hex(data)}")
# sleep(1)

# ASICrevision ID
data = i2cbus.read_byte_data(i2caddress, 0x01)
print(f"REVID (Read): {hex(data)}")
# sleep(1)

# Status
data = i2cbus.read_byte_data(i2caddress, 0x03)
print(f"STATUS (Read): {hex(data)}")
# sleep(1)

# Control
data = 0xA8
i2cbus.write_byte_data(i2caddress, 0x02, data)
print(f"CTRL (Write): {hex(data)}")
# sleep(1)
data = i2cbus.read_byte_data(i2caddress, 0x02)
print(f"CTRL (Read): {hex(data)}")
# sleep(1)

# Status, it should be read as 0x00 at this point
data = i2cbus.read_byte_data(i2caddress, 0x03)
print(f"STATUS (Read): {hex(data)}")
# sleep(1)

data = 0x05
i2cbus.write_byte_data(i2caddress, 0x09, data)
print(f"MDTHR (Write): {hex(data)}")
# sleep(1)
data = i2cbus.read_byte_data(i2caddress, 0x09)
print(f"MDTHR (Read): {hex(data)}")

data = 0x30
i2cbus.write_byte_data(i2caddress, 0x0A, data)
print(f"MDFFTHR (Write): {hex(data)}")
# sleep(1)
data = i2cbus.read_byte_data(i2caddress, 0x0A)
print(f"MDFFTHR (Read): {hex(data)}")

for i in range(30):
    data = i2cbus.read_byte_data(i2caddress_1, 0x00)
    print(f"INT STATUS (Read): {hex(data)}")

    data = i2cbus.read_byte_data(i2caddress, 0x05)
    print(f"INT STATUS (Read): {hex(data)}")

    j = i % 3
    i2cbus.write_byte_data(i2caddress_2, 0x00, j)
    # sleep(1)
    byte_list = i2cbus.read_i2c_block_data(i2caddress_2, 0x00, 32)
    char_array = "".join(chr(byte) for byte in byte_list)
    print(f"Converted character array: {char_array}")

    sleep(1)

led.off()
