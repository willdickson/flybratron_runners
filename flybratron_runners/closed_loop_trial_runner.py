from __future__ import print_function
import copy
import time
import random
from flybratron_trial_runner import FlybratronTrialRunner


class ClosedLoopTrialRunner(FlybratronTrialRunner):


    def __init__(self, param):
        """
        TODO:  document param for AmplitudeTrialRunner
        """
        super(ClosedLoopTrialRunner, self).__init__(param)


    def mark_quiet_period(self, start_up=False):
        """
        Set phidget voltage to mark an quiet period and wait for the
        appropriate time period. 
        """
        super(ClosedLoopTrialRunner, self).mark_quiet_period()
        if start_up:
            time.sleep(self.STARTUP_QUIET_DURATION)
        else:
            time.sleep(self.param['trial']['stimulus_off_t'])


    def mark_stimulus(self, sign, duration):
        """
        Set phidget voltage to the amplitude and wait for the appropriate time
        period. 
        """
        self.set_marker_voltage(sign*self.param['voltage_markers']['stimulus'])
        time.sleep(duration)


    def run(self):

        """ 
        Run repetition number of duration trial sets as specified by the user
        in the parameters passed to the trial runner. Each amplitude is run in
        both the left and right directions.
        """

        self.flybratron_dev.phase = self.param['trial']['phase']
        self.flybratron_dev.waveform = self.param['trial']['waveform']
        self.flybratron_dev.gain = float(self.param['trial']['closed_loop']['gain'])
        self.flybratron_dev.offset = float(self.param['trial']['closed_loop']['offset'])
        self.flybratron_dev.amplitude = 0.0
        self.flybratron_dev.operating_mode = 'sync'

        # Set phidiget voltage to mark the start of the set of experiments.
        self.mark_quiet_period(start_up=True)
        self.mark_start_of_experiment()
        self.mark_quiet_period(start_up=True)

        # Repeat set of stimuli for the requested number of repetitions.
        for repetition_number in range(self.param['trial']['repetitions']):  

            # Get simulus presentation parameters
            amplitude = self.param['trial']['amplitude']
            stimulus_on_t = self.param['trial']['stimulus_on_t']
            stimulus_off_t = self.param['trial']['stimulus_off_t']

            # Stimulus directions (left,right), randomize if requested
            left_right_signs = [1, -1] # 1 = left,-1 = right
            if self.param['trial']['randomize']['left_right']:
                random.shuffle(left_right_signs)

            # Loop over amplitude signs (left & right) which are optionally randomized.
            for sign in left_right_signs:
                amplitude_w_sign = sign*amplitude
                print('rep#: {}/{}, amplitude: {}, on_t: {}, off_t: {}'.format(
                    repetition_number, 
                    self.param['trial']['repetitions'],
                    amplitude_w_sign, 
                    stimulus_on_t, 
                    stimulus_off_t,
                    ))

                # Closed loop (zero amplitude) period
                self.flybratron_dev.amplitude = 0.0
                self.flybratron_dev.operating_mode = 'closed_loop'
                self.mark_quiet_period()

                # Open loop stimulus period with some user set amplitude
                self.flybratron_dev.operating_mode = 'sync'
                self.flybratron_dev.amplitude = amplitude_w_sign
                self.mark_stimulus(sign, stimulus_on_t)

            print()

        # One final closed loop peroid after last open loop stimulus
        self.flybratron_dev.operating_mode = 'closed_loop'
        self.flybratron_dev.amplitude = 0.0
        self.mark_quiet_period(stimulus_off_t)
        self.flybratron_dev.operating_mode = 'sync'

        










