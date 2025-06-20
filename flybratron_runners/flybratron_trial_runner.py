from __future__ import print_function
import flybratron
from trial_runner import TrialRunner


class FlybratronTrialRunner(TrialRunner):
    
    """
    Base class for trial runners using flybratron.
    """

    def __init__(self, param):
        """
        TODO:  document param for TrialRunner
        """
        super(FlybratronTrialRunner, self).__init__(param)
        self.flybratron_dev = None
        self.setup_flybratron()


    def setup_flybratron(self):
        """ 
        Create Flybratron device object and set initial values 
        """
        self.flybratron_dev = flybratron.Flybratron(self.param['hardware']['flybratron_port'])
        self.flybratron_dev.param = {
            'amplitude': 0.0,
            'phase': 0.0,
            'operating_mode': 'sync',
            'amplitude_mode': 'angvel', 
        }


    def clean_up(self, print_info=True):
        """
        Put flybratron hardware into known state,  clean up all hardware objects and
        shutdown rosbag recording.
        """
        if self.flybratron_dev is not None:
            self.flybratron_dev.amplitude = 0.0
            self.flybratron_dev.phase = 0.0
            self.flybratron_dev.close()
            self.flybratron_dev = None
        super(FlybratronTrialRunner, self).clean_up(print_info=print_info)
