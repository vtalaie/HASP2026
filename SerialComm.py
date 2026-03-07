import serial
import select
import os
import signal

class SerialComm:
    def __init__(self):
        self.__currentCommand = bytearray()
        self.__currentPlatformData = bytearray()
        self.__ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE, parity='N')

    @property
    def currentCommand(self):
        return self.__currentCommand

    @property
    def currentPlatformData(self):
        return self.__currentPlatformData

    @property
    def isOpen(self):
        return self.__ser.isOpen()

    def StartComm(self):
        global ser
        global previousdata
        previousData = 0
        global serialFrame
        serialFrame = bytearray()

        try:
            # Open serial port in non-blocking mode (timeout=0)
            #self.__ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE, parity='N')
            serial_fd = self.__ser.fileno()
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            exit()

        epoll = select.epoll()

        # Register serial port FD for input events
        epoll.register(serial_fd, select.EPOLLIN)

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
                                #serialFrame.append(data[0])
                                serialFrame += data

                                if ((b'\r' in serialFrame) and (b'\n' in serialFrame)):
                                    temp = bytearray()
                                    temp[:] = serialFrame
                                    search_string = "$GPGGA"
                                    search_bytes = search_string.encode('utf-8')
                                    position = temp.find(search_bytes)
                                    if (position != -1):
                                        self.__currentPlatformData = temp
                                        #print(self.__currentPlatformData)
                                    else:
                                        self.__currentCommand = temp
                                        #print(self.__currentCommand)
                                    serialFrame.clear()
 
                                #if ((previousData == b'\r') and (data == b'\n')):
                                #    print("Serial Frame Received")
                                #    temp = bytearray()
                                #    temp[:] = serialFrame
                                #    search_string = "$GPGGA"
                                #    search_bytes = search_string.encode('utf-8')
                                #    position = temp.find(search_bytes)
                                #    if (position != -1):
                                #        self.__currentCommand = temp
                                #        print(self.__currentCommand)
                                #    else:
                                #        self.__currentPlatformData = temp
                                #        print(self.__currentPlatformData)
                                #    serialFrame.clear()
                                #previousData = data
                    break

        except KeyboardInterrupt:
            self.__currentCommand
            self.__currentPlatformData
        finally:
            # Clean up
            epoll.unregister(serial_fd)
            epoll.close()
            ser.close()

    def StopComm(self):
        pid = os.getpid()
        os.kill(pid, signal.SIGINT)

    def WriteToComm(self, data_array: bytearray):
        global ser
        if (self.__ser.is_open):
            self.__ser.write(data_array)
        None

def main():
    serialComm = SerialComm()
    serialComm.StartComm()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program.")
