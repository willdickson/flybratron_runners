import numpy as np
from flybratron_runners import PhaseTrialRunner

param = {
        'hardware' : {
            'flybratron_port' : '/dev/ttyACM0',
            'phidget_serial'  : 525467,
            'phidget_channel' : 1, 
            },
        'metadata' : {
            'driver'    : 'XHCS',
            'responder' : 'XHCS',
            'user_tag'  : 'YPMS',
            }, 
        'recording' : {
            'enabled'     : True, 
            'bagfile_dir' : '/home/fponce/bagfiles/ivo/',
            'launch_file' : '/home/fponce/catkin_ws/src/Kinefly/launch/record.launch'
            },
        'trial' :{
            'phases'         : np.linspace(-0.125, 0.125, 11), 
            'amplitude'      : 1000,   
            'waveform'       : 'sin2f',
            'repetitions'    : 1,  
            'stimulus_on_t'  : 0.25, 
            'stimulus_off_t' : 0.75, 
            },
        'voltage_markers' : {
            'start_of_experiment' : -8.2, 
            'quiet_period'        : -9.0, 
            'phase_to_volt'       : lambda phase : 10*phase, 
            },
        }

runner = PhaseTrialRunner(param)
runner.run()
runner.clean_up()
