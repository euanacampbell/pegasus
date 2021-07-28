import os
from shutil import copy
import sys



class lockscreen:
    """Update lockscreen wallpaper. Commands: default, update"""

    def __init__(self, config=None):
        self.config = config

    def __run__(self, param=["default"]):
        if param==[]:
            param=["default"]
        temp_location = "C:\Temp"
        master_location = "C:\Temp\wallpaper_backup\master"
        master_file_name = "Squares.jpg"
        backup = "C:/Temp/wallpaper_backup"
        temp_contents = [i for i in os.listdir(temp_location) if i.endswith('.jpg')]
        backup_contents = [i for i in os.listdir(backup) if i.endswith('.jpg')]


        print(temp_contents)

        if param[0]=='default':
            print('setting back to default wallpaper')
            for file_name in temp_contents:
                    os.remove(f'{temp_location}\{file_name}')

            for file_name in backup_contents:
                copy(f"{backup}\{file_name}", temp_location)
        elif param[0]=='update':
            print('adding your choice of wallpaper')
            # backup all wallpapers
            for file_name in temp_contents:
                # copy subdirectory example
                file_path = f"{temp_location}\{file_name}"
                
                if not os.path.isfile(f"{backup}/{file_name}"):
                    print(f"{file_name} being copied")
                    copy(file_path, backup)


            # replace default wallpapers with the master
            
            for file_name in temp_contents:
                copy(f"{master_location}\{master_file_name}", temp_location)
                
                if file_name != master_file_name:
                    os.remove(f'{temp_location}\{file_name}')
                    os.rename(f'{temp_location}\{master_file_name}', f'{temp_location}\{file_name}')
