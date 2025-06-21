
# Utility functions
def index_to_volts(v_step=0.2, v_offset=2.5):
    """ 
    Returns a fuction for converting an index to a voltage based on the given
    step and offset parametes.  
    f"""
    def index_to_volts_func(index):
        return v_step*index + v_offset
    return index_to_volts_func
