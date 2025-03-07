from serial.tools.list_ports_common import ListPortInfo
import serial

from .stimjim import StimJim, PulseTrain, PulseStage, StimJimOutputModes, STIMJIM_SERIAL_BAUDRATE

class ApplicationConfiguration:

    #The name of the application
    appname: str = "H-Reflex Conditioning"

    #The author/organization of the application
    appauthor: str = "TxBDC"

    #StimJim serial connection
    stimjim_serial: serial.Serial = None

    #StimJim object
    stimjim: StimJim = None

    #region Methods

    @staticmethod
    def connect_to_stimjim (port: ListPortInfo) -> None:
        ApplicationConfiguration.stimjim_serial = serial.Serial(port, baudrate = STIMJIM_SERIAL_BAUDRATE)
        ApplicationConfiguration.stimjim = StimJim(ApplicationConfiguration.stimjim_serial)

    @staticmethod
    def disconnect_from_stimjim () -> None:
        if (ApplicationConfiguration.stimjim_serial is not None):
            if (ApplicationConfiguration.stimjim_serial.is_open):
                ApplicationConfiguration.stimjim_serial.close()
        
        ApplicationConfiguration.stimjim = None

    @staticmethod
    def set_monophasic_stimulus_pulse_parameters_on_stimjim (amplitude_ma: float) -> None:
        #Standard VNS parameters:
        #   Current = decided by the caller of the function
        #   Frequency = N/A
        #   Pulse phase width = 500 us
        #   Monophasic pulse
        #   Train duration = 500 us
        #   Total pulses = 1

        #StimJim command:
        #S0,1,3,0,500; X,0,500;
        #See the documentation for how this command is composed:
        #   https://github.com/open-ephys/stimjim

        #Calculate the amplitude in microamps
        ampltidue_ua: int = int(amplitude_ma * 1000.0)

        #Create two pulse stages
        pulse_stage_01: PulseStage = PulseStage(ampltidue_ua, 0, 500)

        #Create the pulse train
        pulse_train: PulseTrain = PulseTrain(0, 0, 500, 
            [StimJimOutputModes.CURRENT, StimJimOutputModes.GROUNDED],
            [pulse_stage_01])

        #Set the stimulation parameters on the StimJim
        stimjim_cmd_str: str = pulse_train.get_stimjim_string()

        if (ApplicationConfiguration.stimjim is not None):
            ApplicationConfiguration.stimjim.pulse_trains[0] = pulse_train
            ApplicationConfiguration.stimjim.send_command(stimjim_cmd_str)

        pass

    @staticmethod
    def set_standard_vns_stimulation_parameters_on_stimjim () -> None:
        #Standard VNS parameters:
        #   Current = 0.8 mA (800 uA)
        #   Frequency = 30 Hz
        #   Pulse phase width = 100 us
        #   Biphasic pulse
        #   Train duration = 500 ms (500000 microseconds)
        #   Total pulses = 15
        #   Pulses are delivered every 33.333 ms (or 33333 microseconds)

        #StimJim command:
        #S0,1,3,33333,500000; 800,0,100; -800,0,100
        #See the documentation for how this command is composed:
        #   https://github.com/open-ephys/stimjim

        #Create two pulse stages
        pulse_stage_01: PulseStage = PulseStage(800, 0, 100)
        pulse_stage_02: PulseStage = PulseStage(-800, 0, 100)

        #Create the pulse train
        pulse_train: PulseTrain = PulseTrain(0, 33333, 500000, 
            [StimJimOutputModes.CURRENT, StimJimOutputModes.GROUNDED],
            [pulse_stage_01, pulse_stage_02])

        #Set the stimulation parameters on the StimJim
        stimjim_cmd_str: str = pulse_train.get_stimjim_string()

        if (ApplicationConfiguration.stimjim is not None):
            ApplicationConfiguration.stimjim.pulse_trains[0] = pulse_train
            ApplicationConfiguration.stimjim.send_command(stimjim_cmd_str)

        pass

    #endregion