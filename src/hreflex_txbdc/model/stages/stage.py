from PySide6.QtCore import Signal, QObject
import pyqtgraph as pg
import numpy as np

class StageSignals (QObject):

    #region Signals

    new_message = Signal(object)

    #endregion

class Stage (object):

    #region Constants

    #The EMG samples/second
    SAMPLE_RATE: int = 5000

    #A fake-enumeration of stage types
    STAGE_TYPE_EMG_CHARACTERIZATION: int = 0
    STAGE_TYPE_RECRUITMENT_CURVE: int = 1
    STAGE_TYPE_EXPERIMENT: int = 2

    #endregion

    #region Constructor

    def __init__(self):

        #Define the signals for the stage
        self.signals = StageSignals()
        
        #Define the stage name
        self.stage_name: str = ""

        #Define the stage description
        self.stage_description: str = ""

        #Define the stage type
        self.stage_type: int = Stage.STAGE_TYPE_EMG_CHARACTERIZATION

        #Define null values for the session and trial widgets
        self._session_widget: pg.PlotWidget = None
        self._trial_widget: pg.PlotWidget = None

        #Set the subject name
        self._subject_id: str = ""

        #Set the trial plot index and session plot index
        self._trial_plot_index: int = 0
        self._session_plot_index: int = 0

    #endregion

    #region Properties

    @property
    def trial_plot_index(self) -> int:
        return self._trial_plot_index
    
    @trial_plot_index.setter
    def trial_plot_index(self, value: int) -> None:
        self._trial_plot_index = value
        self.update_trial_plot()

    @property
    def session_plot_index(self) -> int:
        return self._session_plot_index
    
    @session_plot_index.setter
    def session_plot_index(self, value: int) -> None:
        self._session_plot_index = value
        self.update_session_plot()

    #endregion

    #region Methods

    def initialize (self, subject_id: str) -> tuple[bool, str]:
        
        #This should be implemented by each stage

        #The function returns a tuple containing a boolean and a string.
        #If all necessary criteria are met to properly run the stage,
        #then the tuple should contain a value of True for the boolean. The 
        #string value can be lefty empty.
        #If NOT all necessary criteria are met to propelry run the stage,
        #then the tuple should contain a value of False for the boolean. The
        #string value should contain an informative message to the user
        #that explains why the stage cannot be run.

        return (True, "")

    def process (self, data: np.ndarray) -> None:

        #This should be implemented by each stage

        return
    
    def input (self, user_input: str) -> None:

        #This should be implemented by each stage

        return

    def set_session_and_trial_widgets (self, session_widget: pg.PlotWidget, trial_widget: pg.PlotWidget) -> None:
        '''
        The UI calls this method to set the session and trial widgets on the stage object.
        This allows each stage to plot information on these widgets in a customized, personalized way.
        '''

        self._session_widget = session_widget
        self._trial_widget = trial_widget

    def finalize (self) -> None:

        #This should be implemented by each stage

        pass

    def get_trial_plot_options (self) -> list[str]:
        
        #This should be implemented by each stage

        return []
    
    def get_session_plot_options (self) -> list[str]:

        #This should be implemented by each stage

        return []
    
    def update_trial_plot (self) -> None:

        #This should be implemented by each stage

        pass

    def update_session_plot (self) -> None:

        #This should be implemented by each stage

        pass

    #endregion

