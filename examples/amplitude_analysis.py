from flybratron_runners import AmplitudeTrialRunner
from flybratron_runners import index_to_volts

param = {
        'hardware' : {
            'flybratron_port' : '/dev/ttyACM0',
            'phidget_serial'  : 525467,
            'phidget_channel' : 1, 
            },
        'metadata' : {
            'driver'    : 'XHCS',
            'responder' : 'XHCS',
            'user_tag'  : 'YAMS',
            }, 
        'recording' : {
            'enabled'     : True, 
            'bagfile_dir'  : '/home/fponce/bagfiles/ivo/',
            'launch_file'  : '/home/fponce/catkin_ws/src/Kinefly/launch/record.launch'
            },
        'trial' :{
            'phase'          : -0.05, 
            'amplitudes'     : [200, 400, 600, 800, 1000, 1200, 1400, 1600],   
            'waveform'       : 'sin2f',
            'repetitions'    : 1,  
            'stimulus_on_t'  : 0.25, 
            'stimulus_off_t' : 0.75, 
            'randomize'      : {
                'amplitudes' : True,
                'left_right' : True,
                }, 
            },
        'voltage_markers' : {
            'start_of_experiment'     : -8.2, 
            'quiet_period'            : -9.0, 
            'amplitude_index_to_volt' : index_to_volts(v_step=0.2, v_offset=2.5),  
            },
        }


runner = AmplitudeTrialRunner(param)
runner.run()
runner.clean_up()
