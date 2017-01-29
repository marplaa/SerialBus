VALUE_TYPE_FLAG = 0
VALUE_TYPE_BYTE = 1
VALUE_TYPE_INT = 2
VALUE_TYPE_FLOAT = 3

DATA_TYPE_BYTE = 0
DATA_TYPE_INT = 1
DATA_TYPE_FLOAT = 2
DATA_TYPE_STRING = 3

# value_ids
DATA = 0
LOW_THRES = 1 
HIGH_THRES = 2
MIN_IMPULSE_LENGTH = 3
MIN_IDLE_LENGTH = 4 
MAX_FAILS = 5 
HYSTERESIS = 6
INTERVAL = 7
INVERT = 8
SENSOR_VALUE = 16


value_id_type_map = {DATA:               VALUE_TYPE_INT,
                     LOW_THRES:          VALUE_TYPE_INT,
                     HIGH_THRES:         VALUE_TYPE_INT,
                     MIN_IMPULSE_LENGTH: VALUE_TYPE_INT,
                     MIN_IDLE_LENGTH:    VALUE_TYPE_INT,
                     MAX_FAILS:          VALUE_TYPE_BYTE,
                     HYSTERESIS:         VALUE_TYPE_BYTE,
                     INTERVAL:           VALUE_TYPE_BYTE,
                     INVERT:             VALUE_TYPE_FLAG,
                     SENSOR_VALUE:       VALUE_TYPE_INT}

def get_value_types():
    """return a dictionary of value_id:value_type pairs"""
    return value_id_type_map

def get_data_type():
    """return a dictionary of value_id:value_type pairs"""
    return 1 #for integer
