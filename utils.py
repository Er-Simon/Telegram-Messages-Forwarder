import consts
import json
import os

from datetime import datetime

def loads_data():
    data = None
    
    if os.path.exists(consts.CONFIG_FILE_PATH):
        with open(consts.CONFIG_FILE_PATH, "r") as f_in:
            data = json.loads(f_in.read())
            
    return data

def dumps_data(data):
    with open(consts.CONFIG_FILE_PATH, "w") as f_out:
        f_out.write(json.dumps(data, indent=2))
        
def get_current_datetime_str():
    return datetime.now(consts.TZ_INFO).strftime(consts.DATETIME_FORMAT)