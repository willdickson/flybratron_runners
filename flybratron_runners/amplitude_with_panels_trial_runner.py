from __future__ import print_function
from amplitude_trial_runner import AmplitudeTrialRunner
from panels_trial_runner import PanelsTrialRunner

class AmplitudeWithPanelsTrialRunner(AmplitudeTrialRunner,PanelsTrialRunner):

    def __init__(self, param):
        AmplitudeTrialRunner.__init__(self,param)
        PanelsTrialRunner.__init__(self,param)

    def run(self):
        """ 
        Run repetitis number of amplitudes trials specified by the user in the
        parameters passed to the trial runner. Each amplitude is run in both
        the left and right directions.
        """
        self.flybratron_dev.phase = self.param['trial']['phase']
        self.flybratron_dev.waveform = self.param['trial']['waveform']
        self.flybratron_dev.amplitude = 0.0

        self.panel_comm.stop()
        self.panel_comm.all_off()
        self.panel_comm.set_gain_bias(0,0,0,0)
        self.panel_comm.set_pattern_id(self.param['trial']['panels_pattern_id'])

        # Set phidiget voltage to mark the start of the set of experiments.
        self.mark_quiet_period(start_up=True)
        self.mark_start_of_experiment()
        self.mark_quiet_period(start_up=True)

        # Repeat set of amplitudes for the requested number of repetitions.
        for repetition_number in range(self.param['trial']['repetitions']):  

            # Get copy of lists of amplitudes and panels_biases
            amplitude_list = list(self.param['trial']['amplitudes'])
            panels_bias_list = list(self.param['trial']['panels_biases'])

            # Loop over amplitudes and biases and present each in order
            for amplitude, panels_bias in zip(amplitude_list, panels_bias_list):
                print('rep#: {}/{}, amplitude: {},panels'.format(
                    repetition_number, 
                    self.param['trial']['repetitions'], 
                    amplitude,
                    panels_bias,
                    ))

                # Stimulus period
                self.flybratron_dev.amplitude = amplitude
                self.panel_comm.set_gain_bias(0,panels_bias,0,0)
                self.panel_comm.start()
                self.mark_amplitude(amplitude)

                # Quiet period
                self.flybratron_dev.amplitude = 0.0
                self.panel_comm.stop()
                self.panel_comm.set_gain_bias(0,0,0,0)
                self.mark_quiet_period()
            print()


