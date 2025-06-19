from flybratron_runners import DurationTrialRunner

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
            'repetitions'       : 1,  
            'stimulus_t'        : [
                {'on': 0.125, 'off' : 1.0}, 
                {'on': 0.250, 'off' : 1.0}, 
                {'on': 0.50,  'off' : 1.0}, 
                {'on': 1.0,   'off' : 1.0}, 
                {'on': 2.0,   'off' : 1.0}, 
                {'on': 4.0,   'off' : 1.0}, 
                ],
            'randomize'         : {
                'stimulus_t'    : False,
                'left_right'    : False,
                }, 
            },
        'voltage_markers' : {
            'start_of_experiment' : -8.2, 
            'quiet_period'        : -9.0, 
            'stimulus'            : 2.5,  
            },
        }

runner = DurationTrialRunner(param)
runner.run()
runner.clean_up()
