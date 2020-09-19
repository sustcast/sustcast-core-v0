from datetime import datetime
import os


ISOFORMAT = '%Y-%m-%dT%H:%M:%S'
PROGRAM_LIST_CSV_PATH = 'content/program_schedule.csv'
PROGRAM_CONTENT_ROOT_PATH = 'content/programs/'
TAG = "@SCHEDULER>"


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

    program_list = get_program_schedule()


    flag_program = False
    index = 0
    while index < len(program_list):
        program  = program_list[index]

        time_diff = 0

        if program["status"] == '0':
            current_time = datetime.now()
            program_time = datetime.strptime(program['time'], ISOFORMAT)

            time_diff = (program_time - current_time).total_seconds()

            if time_diff < 400:
                music = {
                    "title_show" : program["title"],
                    "duration" : program["duration"],
                    "file" : PROGRAM_CONTENT_ROOT_PATH + program['file']
                }

                program_list[index]['status'] = '1'
                flag_program = True

        index = index + 1 

        if flag_program == True:
            print(TAG," --- got a program --- " + program["time"])
            print(TAG," --- delay of program --- " + str(time_diff)) 
            break
    
    if flag_program == True:
        update_program_schedule(program_list)
    
    elif flag_program == False :
        music = Recommender.recommend()

    return music

def get_program_schedule():
    return CsvUtils.readDataFromCsv(PROGRAM_LIST_CSV_PATH)

def update_program_schedule(program_list):
    return CsvUtils.writeDataToCsv(PROGRAM_LIST_CSV_PATH,program_list)



