from flybratron_runners import ClosedLoopTrialRunner

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
            'phase'             : -0.05, 
            'amplitude'         : 1000,   
            'waveform'          : 'sin2f',
            'repetitions'       : 10,  
            'stimulus_on_t'     : 0.125, 
            'stimulus_off_t'    : 0.750,
            'closed_loop'       : {
                'gain'          : 5000,
                'offset'        : 0, 
                }, 
            'randomize'         : {
                'left_right'    : False,
                }, 
            },
        'voltage_markers' : {
            'start_of_experiment' : -8.2, 
            'quiet_period'        : -9.0, 
            'stimulus'            : 2.5,  
            },
        }

runner = ClosedLoopTrialRunner(param)
runner.run()
runner.clean_up()
