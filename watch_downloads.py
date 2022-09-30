from watchfiles import watch
from datetime import datetime
import os
from pydantic import BaseSettings
from urllib import parse

class Settings(BaseSettings):
    log_url: str
    watch_dir: str
    dest_dir_root: str
    class Config:
            env_file = ".env"

settings = Settings()

# if watch url == log url get a new one

def get_log():
     with open(f'{settings.log_url}/changes.txt', 'r') as log:
           data = log.read()
           return data

def write_log(entry):
        with open(f'{settings.log_url}/changes.txt', 'w') as log:
            log.write(f"{data}\n{entry}")


for changes in watch(settings.watch_dir):
    
    now = datetime.now()
    data = get_log()

    # loop set returned by watch
    for entry in changes:
        
        # variables
        action = str(entry[0]).split('.')[1]
        file_path = entry[1]
        file_name = os.path.basename(file_path)
        log_entry = f"{str(now)[0:str(now).find('.', 0)]} -- {file_path} ---> {action}"
        
        print(file_name)
        # first log files
        write_log(log_entry)


        if file_path.endswith("txt") and action == "added":
            os.rename(file_path, f'C:/Users/willm/Desktop/watchgod/test/{file_name}')

# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
#  f"{settings.dest_dir_root}/"