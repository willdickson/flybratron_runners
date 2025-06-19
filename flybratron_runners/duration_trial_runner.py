from __future__ import print_function
import copy
import time
import random
from trial_runner import TrialRunner


class DurationTrialRunner(TrialRunner):

    STARTUP_QUIET_DURATION = 0.75

    def __init__(self, param):
        """
        TODO:  document param for AmplitudeTrialRunner
        """
        super(DurationTrialRunner, self).__init__(param)

    def mark_quiet_period(self, duration):
        """
        Set phidget voltage to mark an quiet period and wait for the
        appropriate time period. 
        """
        super(DurationTrialRunner, self).mark_quiet_period()
        time.sleep(duration)


    def mark_stimulus(self, duration):
        """
        Set phidget voltage to the amplitude and wait for the appropriate time
        period. 
        """
        self.set_marker_voltage(self.param['voltage_markers']['stimulus'])
        time.sleep(duration)

    def run(self):

        """ 
        Run repetition number of duration trial sets as specified by the user
        in the parameters passed to the trial runner. Each amplitude is run in
        both the left and right directions.
        """

        self.flybratron_dev.phase = self.param['trial']['phase']
        self.flybratron_dev.waveform = self.param['trial']['waveform']
        self.flybratron_dev.amplitude = 0.0

        # Set phidiget voltage to mark the start of the set of experiments.
        self.mark_quiet_period(self.STARTUP_QUIET_DURATION)
        self.mark_start_of_experiment()
        self.mark_quiet_period(self.STARTUP_QUIET_DURATION)

        # Repeat set of amplitudes for the requested number of repetitions.
        for repetition_number in range(self.param['trial']['repetitions']):  

            # Get copy of list of stimulus times (on and off) and (optionaly) shuffle the list
            stimulus_t_list = copy.copy(self.param['trial']['stimulus_t'])
            if self.param['trial']['randomize']['stimulus_t']:
                random.shuffle(stimulus_t_list)

            # Loop over stimulus times and present amplitude in the both directions
            for stimulus_t in stimulus_t_list:
                left_right_signs = [1, -1] # 1 = left,-1 = right
                if self.param['trial']['randomize']['left_right']:
                    random.shuffle(left_right_signs)
                amplitude = self.param['trial']['amplitude']

                # Loop over amplitude signs (left & right) which are optionally randomized.
                for sign in left_right_signs:
                    amplitude_w_sign = sign*amplitude
                    print('rep#: {}, ampitude: {}, on_t: {}, off_t: {}'.format(
                        repetition_number, 
                        amplitude_w_sign, 
                        stimulus_t['on'], 
                        stimulus_t['off'],
                        ))
                    self.flybratron_dev.amplitude = amplitude_w_sign
                    self.mark_stimulus(stimulus_t['on'])
                    self.flybratron_dev.amplitude = 0.0
                    self.mark_quiet_period(stimulus_t['off'])
            print()










