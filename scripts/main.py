import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from hreflex_txbdc.view.main_window import MainWindow
from hreflex_txbdc.model.stimjim import discover_ports
from hreflex_txbdc.model.application_configuration import ApplicationConfiguration
from serial.tools.list_ports_common import ListPortInfo
import serial

REQUIRE_STIMJIM: bool = False

def main () -> None:
    #Create the QT application
    app = QtWidgets.QApplication(sys.argv)

    #Discover serial ports that match the StimJim hardware
    possible_ports: list[ListPortInfo] = discover_ports()

    #Check to see if any ports matching the StimJim were discovered
    if REQUIRE_STIMJIM and (len(possible_ports) == 0):
        #If not, display an error message to the user
        #and then return immediately.
        dlg: QMessageBox = QMessageBox()
        dlg.setWindowTitle("Error! StimJim not detected!")
        dlg.setText("The application was unable to detect a StimJim connected to the computer. The application cannot proceed.")
        dlg.exec()

        return

    #Connect to the StimJim
    if (len(possible_ports) > 0):
        ApplicationConfiguration.connect_to_stimjim(possible_ports[0].device)

    #Instantiate the MainWindow object
    window = MainWindow()

    #Display the main window
    window.show()

    #Turn control over to QT's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


# import serial
# import time
# import PySide6.QtWidgets
# import sys
# from serial.tools.list_ports_common import ListPortInfo
# # Define serial port (adjust the port according to your system, e.g., COM9 on Windows or /dev/ttyUSB0 on Linux)
# # ser = serial.Serial('COM9', baudrate=9600, timeout=1)  # Replace with your correct port

# # # Function to send command to Arduino
# # def send_command(command):
# #     ser.write((command + '\n').encode())
# #     print(f"Sent command: {command}")

# # # Main program
# # if __name__ == "__main__":
# #     # Send the first command to Arduino
# #     send_command("S0,1,0,33333,50000000;800,5000,100;-800,5000,100")

# #     # Wait for a short period before sending the next command
# #     time.sleep(1)  # You can adjust the delay as needed

# #     # Send the second command to Arduino
# #     send_command("T0")
    
# #     # Optionally, you can loop to continuously send commands or trigger other actions
# #     # For example, to continuously send commands every 5 seconds:
# #     while True:
# #         send_command("T0")  # Send "T0" to Arduino
# #         time.sleep(5)  # Wait 5 seconds before sending the next command


# app = PySide6.QtWidgets.QApplication(sys.argv)
# label = PySide6.QtWidgets.QLabel("Hello World!")
# label.show()
# app.exec()

# #https://github.com/picotech/picosdk-python-wrappers
