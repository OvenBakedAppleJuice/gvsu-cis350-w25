import serial
import threading
from queue import Queue
import time

class USBComm:
    def __init__(self, dataQueue, LoopDelay, Port='COM8'):
        self.arduino = serial.Serial(port=Port, baudrate=1000000, timeout=0.01)
        self.dataQueue = dataQueue
        self.LoopDelay = LoopDelay
        self.GreenBtn = False
        self.thread = None
        self.__runing = False

    def start(self):
        self.__runing = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        print("Serial Communication Stoped")
        self.__runing = False

    def run(self):
        print("Serial Communication Started")
        while True:
            if not self.dataQueue.empty():
                arduinoData = self.dataQueue.get()

                #empty receiver queue
                while not self.dataQueue.empty():
                    self.dataQueue.get()

                #Send the information, send a header first
                self.arduino.write(b'\xDE\xAD\xBE\xEF')

                #64 bytes that are sent to arduino
                self.arduino.write(arduinoData)

                #Get Button From ESP32
                self.GreenBtn = False
                try:
                    pySerialInput = self.arduino.readline()
                    pySerialInput = int(pySerialInput[0])-48
                    if pySerialInput == 1:
                        self.GreenBtn = True
                        break
                except:
                    None
            else:
                time.sleep(self.LoopDelay)

            if not self.__runing:
                break
