import serial
import serial.tools.list_ports

class USBComm:
    def __init__(self):
        self.__arduino = None

    def startComm(self, Port):
        self.__arduino = serial.Serial(port=Port, baudrate=57600, timeout=0.01)

    def getPortDesciptions(self):
        """
        Lists available serial ports with their descriptions and hardware IDs.
        Returns list of descriptions ex.) [''].
        """
        ports = serial.tools.list_ports.comports()

        if not ports:
            print("No serial ports found.")
            return []

        print("Available Serial Ports:")
        port_list = []
        for port in sorted(ports):
            print(f"  Port: {port.device}")
            print(f"    Description: {port.description}")
            print(f"    Hardware ID: {port.hwid}")
            print("-" * 30)
            port_list.append(port.description)
        
        return port_list

    def getPorts(self):
        """
        Lists available serial ports with their descriptions and hardware IDs.
        Returns list of ports ex.) ['COM3, 'COM15'].
        """
        ports = serial.tools.list_ports.comports()

        if not ports:
            print("No serial ports found.")
            return []

        print("Available Serial Ports:")
        port_list = []
        for port in sorted(ports):
            print(f"  Port: {port.device}")
            print(f"    Description: {port.description}")
            print(f"    Hardware ID: {port.hwid}")
            print("-" * 30)
            port_list.append(port.device)
        
        return port_list

    def run(self, arduinoData):
        #Send the information, send a header first
        self.__arduino.write(b'\xDE\xAD\xBE\xEF')

        #bytes that are sent to arduino
        self.__arduino.write(bytes(arduinoData))

        # try:
        #     pySerialInput = self.__arduino.readline()
        #     pySerialInput = int(pySerialInput[0])-48
        # except:
        #     None
