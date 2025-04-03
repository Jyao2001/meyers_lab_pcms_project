from serial.tools.list_ports_common import ListPortInfo
import serial
import sys
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
import serial.tools.list_ports

# Constants for StimJim device
STIMJIM_SERIAL_BAUDRATE = 115200
STIMJIM_SERIAL_INFO = "VID:PID=16C0:0483"  # This should be the VID:PID of your StimJim device

# Global variable for StimJim serial connection
stimjim_serial: serial.Serial = None

def connect_to_stimjim(port: ListPortInfo) -> None:
    """Connect to the StimJim via the serial port and display connection info."""
    #stimjim_serial = "" # Use the global variable to store the serial connection
    stimjim_serial = serial.Serial(port.device, baudrate=STIMJIM_SERIAL_BAUDRATE, timeout=1)
    print(f"Successfully connected to StimJim on {port.device}")
    print(f"stimjim_serial: {stimjim_serial}")

def discover_ports(pattern=STIMJIM_SERIAL_INFO):
    """Discover serial ports that match the pattern (for StimJim)."""
    ports = list(serial.tools.list_ports.grep(pattern))
    return ports

def main() -> None:
    """Main function to handle connection and display information."""
    # Create the QT application
    app = QApplication(sys.argv)

    # Discover serial ports that match the StimJim hardware
    possible_ports: list[ListPortInfo] = discover_ports()

    # Check to see if any ports matching the StimJim were discovered
    if len(possible_ports) == 0:
        # If no matching device is found, display an error message and return
        dlg = QMessageBox()
        dlg.setWindowTitle("Error!")
        dlg.setText("StimJim not detected. The application cannot proceed.")
        dlg.exec()
        return

    # Connect to the first matching StimJim device
    connect_to_stimjim(possible_ports[0])

    # Show a message box with the connection info
    dlg = QMessageBox()
    dlg.setWindowTitle("Connected!")
    dlg.setText(f"Successfully connected to StimJim on {possible_ports[0].device}")
    dlg.exec()

    # Turn control over to QT's main loop
    #sys.exit(app.exec())

if __name__ == "__main__":
    main()


# import serial
# import time

# # Define serial port (adjust the port according to your system, e.g., COM9 on Windows or /dev/ttyUSB0 on Linux)
# ser = serial.Serial('COM9', baudrate=9600, timeout=1)  # Replace with your correct port

# # Function to send command to Arduino
# def send_command(serial, command):
#     serial.write((command + '\n').encode())
#     print(f"Sent command: {command}")

# # Main program
# if __name__ == "__main__":
#     # Send the first command to Arduino
#     send_command(ser, "S0,1,0,33333,50000000;800,5000,100;-800,5000,100")

#     # Wait for a short period before sending the next command
#     time.sleep(1)  # You can adjust the delay as needed

#     # Send the second command to Arduino
#     send_command(ser, "T0")
    
#     # Optionally, you can loop to continuously send commands or trigger other actions
#     # For example, to continuously send commands every 5 seconds:
#     while True:
#         send_command(ser, "T0")  # Send "T0" to Arduino
#         time.sleep(5)  # Wait 5 seconds before sending the next command


# #https://github.com/picotech/picosdk-python-wrappers