import serial
import serial.tools.list_ports


class USBComm:
    def __init__(self):
        self.__arduino = None

    def startComm(self, port):
        """
        Starts serial communication with the specified port.
        """
        try:
            self.__arduino = serial.Serial(port=port, baudrate=9600, timeout=1)
            print(f"Connected to {port}")
        except serial.SerialException as e:
            print(f"Failed to connect to {port}: {e}")
            self.__arduino = None

    def isConnected(self):
        if self.__arduino is None:
            return False
        elif(isinstance(self.__arduino, serial.Serial)):
            return self.__arduino.is_open
        else:
            return False

    def getPortDescriptions(self):
        """
        Lists available serial ports with their descriptions and hardware IDs.
        Returns list of descriptions, e.g. ['Arduino Uno', 'USB Serial Device'].
        """
        ports = serial.tools.list_ports.comports()

        if not ports:
            print("No serial ports found.")
            return []

        print("Available Serial Ports:")
        port_list = []
        port_str = ""
        for port in sorted(ports):
            port_str = f"Port: {port.device}"
            port_str += f", Description: {port.description}"
            print(port_str)
            port_list.append(port_str)

        return port_list

    def getPorts(self):
        """
        Lists available serial ports.
        Returns list of port names, e.g. ['COM3', 'COM15'].
        """
        ports = serial.tools.list_ports.comports()

        if not ports:
            print("No serial ports found.")
            return []

        port_list = []
        for port in sorted(ports):
            port_list.append(port.device)

        return port_list

    def run(self, arduinoData):
        if self.__arduino is None:
            print("Arduino not connected.")
            return

        try:
            data_str = f"{arduinoData:.2f}\n"  # round to 2 decimal places
            self.__arduino.write(data_str.encode())
            print(f"Sent: {data_str.strip()}")
        except Exception as e:
            print(f"Failed to send data: {e}")

