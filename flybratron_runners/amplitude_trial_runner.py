from __future__ import print_function
import time
import numpy as np
from trial_runner import TrialRunner


class AmplitudeTrialRunner(TrialRunner):

    def __init__(self, param):
        """
        TODO:  document param for AmplitudeTrialRunner
        """
        super(AmplitudeTrialRunner, self).__init__(param)
        self.amplitudes_to_list()

    def mark_quiet_period(self):
        """
        Set phidget voltage to mark an quiet period and wait for the
        appropriate time period. 
        """
        super(AmplitudeTrialRunner, self).mark_quiet_period()
        time.sleep(self.param['trial']['stimulus_off_t'])

    def mark_amplitude(self,amplitude):
        """
        Set phidget voltage to the amplitude and wait for the appropriate time
        period. 
        """
        super(AmplitudeTrialRunner, self).mark_amplitude(amplitude)
        time.sleep(self.param['trial']['stimulus_on_t'])


    def run(self):
        """ 
        Run repetitis number of amplitudes trials specified by the user in the
        parameters passed to the trial runner. Each amplitude is run in both
        the left and right directions.
        """
        self.flybratron_dev.phase = self.param['trial']['phase']
        self.flybratron_dev.waveform = self.param['trial']['waveform']
        self.flybratron_dev.amplitude = 0.0

        # Set phidiget voltage to mark the start of the set of experiments.
        self.mark_quiet_period()
        self.mark_start_of_experiment()
        self.mark_quiet_period()

        # Repeat set of amplitudes for the requested number of repetitions.
        for repetition_number in range(self.param['trial']['repetitions']):  

            # Get copy of list of amplitudes and (optionaly) shuffle the list
            amplitude_list = np.array(self.param['trial']['amplitudes'])
            if self.param['trial']['randomize']['amplitudes']:
                np.random.shuffle(amplitude_list)

            # Loop over amplitudes and present each in the both the and right directions
            for amplitude in amplitude_list:
                left_right_signs = np.array([1, -1]) # 1 = left,-1 = right
                if self.param['trial']['randomize']['left_right']:
                    np.random.shuffle(left_right_signs)

                # Loop over amplitude signs (left & right) which are optionally randomized.
                for sign in left_right_signs:
                    amplitude_w_sign = sign*amplitude
                    print('rep#: {}, ampitude: {}'.format(repetition_number, amplitude_w_sign))
                    self.flybratron_dev.amplitude = amplitude_w_sign
                    self.mark_amplitude(amplitude_w_sign)
                    self.flybratron_dev.amplitude = 0.0
                    self.mark_quiet_period()
            print()

    def amplitudes_to_list(self):
        """
        Make sure trial amplitudes are always a list even though the user may enter
        a numpy array or a single value. 
        """
        try:
            self.param['trial']['amplitudes'] = list(self.param['trial']['amplitudes'])
        except TypeError:
            self.param['trial']['amplitudes'] = list([self.param['trial']['amplitudes']])











