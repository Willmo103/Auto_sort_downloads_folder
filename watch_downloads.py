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

ENV = Settings()

# if watch url == log url get a new one

def get_log():
     with open(f'{ENV.log_url}/changes.txt', 'r') as log:
           data = log.read()
           return data

def write_log(entry):
        with open(f'{ENV.log_url}/changes.txt', 'w') as log:
            log.write(f"{data}\n{entry}")


def make_folder(root, tag):
    folder = f"{root}/{tag}/"
    if os.path.exists(folder):
        pass
    else:
        os.mkdir(folder)
    return folder

for changes in watch(ENV.watch_dir):
    
    now = datetime.now()
    data = get_log()

    # loop set returned by watch
    for entry in changes:
        
        # variables
        action = str(entry[0]).split('.')[1]
        file_path = entry[1]
        file_name = os.path.basename(file_path)

        write_log(f"{str(now)[0:str(now).find('.', 0)]} -- {file_path} ---> {action}")

        if file_path.endswith("txt") and action == "added":
            new_file_path = make_folder(ENV.dest_dir_root, "Documents")
            os.rename(file_path, new_file_path + file_name)

# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
#  f"{settings.dest_dir_root}/"