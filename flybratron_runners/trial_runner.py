from __future__ import print_function
import os
import sys
import time
import datetime
import rospy
import roslaunch 
import Phidget22.Devices.VoltageOutput
import numpy as np
import flybratron


class TrialRunner(object):
    
    """
    Base class for trial runners.
    """

    PHIDGET_ATTACHMENT_WAIT_MS = 5000
    START_OF_EXPERIMENT_MARKER_T = 0.5 # (sec)

    def __init__(self, param):
        """
        TODO:  document param for TrialRunner
        """
        self.param = param
        self.phidget_aout = None
        self.flybratron_dev = None
        self.rosbag_partent = None
        self.rosbag_file_name = ''
        self.rosbag_file_path = ''
        self.setup_phidget_aout()
        self.setup_flybratron()
        self.setup_bagfile_recording()
        self.start_time = time.time()


    def __del__(self):
        self.clean_up(print_info=False)


    def setup_phidget_aout(self):
        """ 
        Setup Phidgets analog output. This voltage is used to indicate the start and
        end of the the recording and well as providing a voltage indicating the current 
        flybratron amplitude.         
        """
        self.phidget_aout = Phidget22.Devices.VoltageOutput.VoltageOutput()
        self.phidget_aout.setDeviceSerialNumber(self.param['hardware']['phidget_serial'])
        self.phidget_aout.setChannel(self.param['hardware']['phidget_channel'])
        self.phidget_aout.openWaitForAttachment(self.PHIDGET_ATTACHMENT_WAIT_MS)
        self.phidget_aout.setEnabled(True)
        self.phidget_aout.setVoltage(0.0)


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


    def setup_bagfile_recording(self):
        """ 
        Starts bagfile recording based on the user's parameters. 
        """
        if not self.param['recording']['enabled']: 
            return 

        if not os.path.exists(self.param['recording']['bagfile_dir']):
            os.makedirs(self.param['recording']['bagfile_dir'])

        # Create bagfile name. Look for files with the same and increment trial
        # number until unused name is found. 
        date_info = datetime.datetime.today().strftime('%y%m%d')
        trial_num = 1
        ok = False
        while not ok:
            file_parts = [date_info] 
            # Add optional driver responder information
            try:
                file_parts.append(self.param['metadata']['driver'])
            except KeyError:
                pass
            try:
                file_parts.append(self.param['metadata']['responder'])
            except KeyError:
                pass

            # Add zero padded trial number
            file_parts.append(str(trial_num).zfill(3))

            # Add optional user tag information
            try:
                file_parts.append(self.param['metadata']['user_tag'])
            except KeyError:
                pass
            base_name = '_'.join(file_parts)
            file_name = '{}.bag'.format(base_name)
            file_path = os.path.join(self.param['recording'] ['bagfile_dir'], file_name)
            if os.path.isfile(file_path):
                trial_num += 1
            else:
                ok = True
            self.rosbag_file_name = file_name
            self.rosbag_file_path = file_path

        # Launch rosbag recording 
        launch_args = 'prefix:={}'.format(file_path)
        sys.argv.append(launch_args)
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False) 
        roslaunch.configure_logging(uuid) 
        launch_files = [self.param['recording']['launch_file']]
        self.rosbag_parent = roslaunch.parent.ROSLaunchParent(uuid, launch_files) 
        rospy.on_shutdown(self.rosbag_parent.shutdown) 
        self.rosbag_parent.start()


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


    def mark_start_of_experiment(self):
        """ 
        Set analog output of Phidget to voltage indicating the start of experiment  
        """
        marker_voltage = self.param['voltage_markers']['start_of_experiment']
        self.set_marker_voltage(marker_voltage)
        time.sleep(self.START_OF_EXPERIMENT_MARKER_T)

    def mark_quiet_period(self):
        """
        Set analog output of Phidget to voltage indicating a quiet period  
        """
        marker_voltage = self.param['voltage_markers']['quiet_period']
        self.set_marker_voltage(marker_voltage)


    def mark_amplitude(self, amplitude):
        """
        Set analog output of Phidget to voltage indicating a specific trial amplitude 
        """
        marker_voltage = self.get_amplitude_marker_voltage(amplitude)
        self.set_marker_voltage(marker_voltage)

    def set_marker_voltage(self, volt):
        """
        Set phidget voltage
        """
        self.phidget_aout.setVoltage(volt)


    def clean_up(self, print_info=True):
        """
        Put hardware into known state,  clean up all hardware objects and
        shutdown rosbag recording.
        """
        # Clean up flybratron
        if self.flybratron_dev is not None:
            self.flybratron_dev.amplitude = 0.0
            self.flybratron_dev.phase = 0.0
            self.flybratron_dev.close()
            self.flybratron_dev = None

        # Clean up phigets analog output
        if self.phidget_aout is not None:
            self.phidget_aout.setVoltage(0.0)
            self.phidget_aout.setEnabled(False)
            self.phidget_aout.close()
            self.phidget_aout = None

        # Shutdown rosbag recording.
        if self.rosbag_parent is not None:
            self.rosbag_parent.shutdown()

        if print_info:
            self.elapsed_time = time.time() - self.start_time
            print('elapsed time: {}'.format(self.elapsed_time))
            print('rogbag file:  {}'.format(self.rosbag_file_path))


# Utility functions
def index_to_volts(v_step=0.2, v_offset=2.5):
    """ 
    Returns a fuction for converting an index to a voltage based on the given
    step and offset parametes.  
    f"""
    def index_to_volts_func(index):
        return v_step*index + v_offset
    return index_to_volts_func
