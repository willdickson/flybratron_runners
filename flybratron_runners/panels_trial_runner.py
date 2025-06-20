from __future__ import print_function
import panel_comm
from trial_runner import TrialRunner


class PanelsTrialRunner(object):

    DEFAULT_SEND_SLEEP_DT = 0.05

    def __init__(self, param):
        self.panel_comm = None
        self.setup_panels()

    def setup_panels(self):
        self.panel_comm = panel_comm.PanelComm(
                self.param['hardware']['panels_port'],
                baudrate = self.param['hardware']['panels_baudrate']
                )
        self.panel_comm.stop()
        self.panel_comm.all_off()
        self.panel_comm.send_sleep_dt = self.DEFAULT_SEND_SLEEP_DT


    def clean_up(self,print_info=True):
        if self.panel_comm is not None:
            self.panel_comm.stop()
            self.panel_comm.set_gain_bias(0,0,0,0)
            self.panel_comm.close()
            self.panel_comm = None
        super(PanelsTrialRunner, self).clean_up(print_info=print_info)


