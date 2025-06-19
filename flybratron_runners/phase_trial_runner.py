from __future__ import print_function
import time
import numpy as np
from trial_runner import TrialRunner


class PhaseTrialRunner(TrialRunner):

    def __init__(self, param):
        super(PhaseTrialRunner, self).__init__(param)

    def mark_quiet_period(self):
        """
        Set phidget voltage to mark an quiet period and wait for the
        appropriate time period. 
        """
        super(PhaseTrialRunner, self).mark_quiet_period()
        time.sleep(self.param['trial']['stimulus_off_t'])


    def mark_phase(self, phase):
        """
        Set phidget voltage to the amplitude and wait for the appropriate time
        period. 
        """
        marker_voltage = self.param['voltage_markers']['phase_to_volt'](phase)
        self.set_marker_voltage(marker_voltage)
        time.sleep(self.param['trial']['stimulus_on_t'])


    def run(self):
        """ 
        Run phase analysis. Loop over array/list of phases and present stimulus in
        both the left and right directions. 
        """
        self.flybratron_dev.waveform = self.param['trial']['waveform']
        self.flybratron_dev.amplitude = 0.0

        # Set phidget voltage to mark the start of the set of experiments.
        self.mark_quiet_period()
        self.mark_start_of_experiment()
        self.mark_quiet_period()

        left_right_signs = np.array([1, -1]) # 1 = left,-1 = right

        # Loop over list of phases to test
        for phase in self.param['trial']['phases']:
            self.flybratron_dev.phase = phase
            amplitude = self.param['trial']['amplitude']

            # Present each phase in the left and right directions
            for sign in left_right_signs:
                amplitude_w_sign = sign*amplitude
                print('amplitude: {} at phase: {}'.format(amplitude_w_sign, phase))
                self.flybratron_dev.amplitude = amplitude_w_sign
                self.mark_phase(phase)
                self.flybratron_dev.amplitude = 0.0
                self.mark_quiet_period()
            print()














