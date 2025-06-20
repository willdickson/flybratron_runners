from __future__ import print_function
import time
import numpy as np
from flybratron_trial_runner import FlybratronTrialRunner


class AmplitudeTrialRunner(FlybratronTrialRunner):

    def __init__(self, param):
        """
        TODO:  document param for AmplitudeTrialRunner
        """
        super(AmplitudeTrialRunner, self).__init__(param)
        self.amplitudes_to_list()


    def mark_quiet_period(self, start_up=False):
        """
        Set phidget voltage to mark an quiet period and wait for the
        appropriate time period. 
        """
        super(AmplitudeTrialRunner, self).mark_quiet_period()
        if start_up:
            time.sleep(self.STARTUP_QUIET_DURATION)
        else:
            time.sleep(self.param['trial']['stimulus_off_t'])


    def mark_amplitude(self, amplitude):
        """
        Set analog output of Phidget to voltage indicating a specific trial amplitude 
        """
        marker_voltage = self.get_amplitude_marker_voltage(amplitude)
        self.set_marker_voltage(marker_voltage)
        time.sleep(self.param['trial']['stimulus_on_t'])


    def get_amplitude_index(self, amplitude):
        """
        Return index of the trial amplitude in the list of amplitudes pass in
        a parameters to the trial runner. If there is no list of amplitudes 
        given the returned index will alway be equal to 0. 
        """
        if not 'amplitudes' in self.param['trial']:
            index = 0
        else:
            index = self.param['trial']['amplitudes'].index(abs(amplitude))
        return index


    def get_amplitude_marker_voltage(self, amplitude): 
        """
        Return the marker voltage for indication of the given amplitude.
        """
        amplitude_index = self.get_amplitude_index(amplitude)
        try:
            index_to_voltage = self.param['voltage_markers']['amplitude_index_to_volt']
        except KeyError:
            marker_voltage = self.param['voltage_marker']['amplitude']
        else:
            marker_voltage = np.sign(amplitude)*index_to_voltage(amplitude_index)
        return marker_voltage


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
        self.mark_quiet_period(start_up=True)
        self.mark_start_of_experiment()
        self.mark_quiet_period(start_up=True)

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
                    print('rep#: {}/{}, amplitude: {}'.format(
                        repetition_number, 
                        self.param['trial']['repetitions'], 
                        amplitude_w_sign
                        ))
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



