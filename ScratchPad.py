import serial
import select
import os
import time
import queue

try:
    # Open serial port in non-blocking mode (timeout=0)
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE, parity='N')
    serial_fd = ser.fileno()
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Create epoll object
epoll = select.epoll()

# Register serial port FD for input events
epoll.register(serial_fd, select.EPOLLIN)

print(f"Monitoring serial port /dev/ttyUSB0...")

serialFrame = bytearray()
global serialQueue
serialQueue = queue.Queue(maxsize=10)
global previousdata
previousdata = 0

try:
    while True:
        # Wait for events with a 1-second timeout
        events = epoll.poll(timeout=1)

        if not events:
            # print("No events, doing other work or just waiting...")
            continue

        for fileno, event in events:
            if fileno == serial_fd:
                if event & select.EPOLLIN:
                    # Read available data
                    # os.read is used with file descriptors
                    data = os.read(fileno, 1024) 
                    if data:
                        # Process the data
                        #decoded_data = data.decode('utf-8').strip()
                        print(f"Received: {data}")
                        serialFrame.append(data[0])
                        if ((previousdata == b'\r') and (data == b'\n')):
                            print("Serial Frame Received")
                            temp = bytearray()
                            temp[:] = serialFrame
                            serialQueue.put(temp)
                            serialFrame.clear()
                        previousdata = data
                        #print(data)
                        # Example: echo back data (optional)
                        # os.write(fileno, data)

except KeyboardInterrupt:
    print("Exiting program.")
    print(serialQueue.qsize())
    while not serialQueue.empty():
        qData = serialQueue.get()
        print(qData)
finally:
    # Clean up
    epoll.unregister(serial_fd)
    epoll.close()
    ser.close()
    print("Serial port and epoll closed.")
