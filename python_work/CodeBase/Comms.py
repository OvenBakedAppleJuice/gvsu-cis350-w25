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
        for port in sorted(ports):
            print(f"  Port: {port.device}")
            print(f"    Description: {port.description}")
            print(f"    Hardware ID: {port.hwid}")
            print("-" * 30)
            port_list.append(port.description)

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
        if self.__arduino is None:
            print("Arduino not connected.")
            return

        try:
            data_str = f"{arduinoData:.2f}\n"  # round to 2 decimal places
            self.__arduino.write(data_str.encode())
            # print(f"Sent: {data_str.strip()}")
        except Exception as e:
            print(f"Failed to send data: {e}")

