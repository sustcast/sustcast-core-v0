from datetime import datetime
import os
import time
from shutil import copyfile
import _thread

ISOFORMAT = '%Y-%m-%dT%H:%M:%S'
PROGRAM_LIST_CSV_PATH = 'content/program_schedule.csv'
PROGRAM_CONTENT_ROOT_PATH = 'content/programs/'
EMERGENCY_PROGRAM_PATH = "content/emergency_program/"
TAG = "@SCHEDULER>"
PROGRAM_QUEUE = []

def set_recommender(module):
    global Recommender
    Recommender = module

def set_modules(helper, csvUtils):
    global Helper
    global CsvUtils
    
    Helper = helper
    CsvUtils = csvUtils


def shuffle():
    music = {}

    # PROGRAM EXISTENCE CHECKING
    program_list = get_program_schedule()

    for program in program_list:

        if program['file'] in PROGRAM_QUEUE:
            continue

        current_time = datetime.now()
        program_time = datetime.strptime(program['time'], ISOFORMAT)
        time_diff = (program_time - current_time).total_seconds()

        if time_diff < 0 :
            continue

        if os.path.isfile(PROGRAM_CONTENT_ROOT_PATH + program['file']) == False:
            print(TAG, "--------------################### FILE DOES NOT EXIST #################------------- => ",program["file"])
            continue

        program_info = {
            "time" : program['time'],
            "file_name" : program['file'],
            "file_path" : PROGRAM_CONTENT_ROOT_PATH + program['file']
        }

        _thread.start_new_thread(run_program_in_specific_time, (program_info,))

        PROGRAM_QUEUE.append(program['file'])

        print(TAG," --- program queue updated--- ")
        print(TAG,PROGRAM_QUEUE)


    
    music = Recommender.recommend()

    return music

def run_program_in_specific_time(program):
    program_time = datetime.strptime(program['time'], ISOFORMAT)
    current_time = datetime.now()
    time_diff = (program_time - current_time).total_seconds()

    print(TAG," --- got a program --- " + program["time"])
    print(TAG,program)
    print(TAG," --- time remaining to broadcast --- " + str(time_diff)) 

    time.sleep(time_diff)

    copyfile(program["file_path"],EMERGENCY_PROGRAM_PATH+"/"+program["file_name"])

    print(TAG," --- program copied to the emergency program folder --- " + program["file_name"])




def get_program_schedule():
    return CsvUtils.readDataFromCsv(PROGRAM_LIST_CSV_PATH)

def update_program_schedule(program_list):
    return CsvUtils.writeDataToCsv(PROGRAM_LIST_CSV_PATH,program_list)



