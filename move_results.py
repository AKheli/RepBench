import shutil
from datetime import datetime
import os

original = "Results"
target = "../../MaResults/"
shutil.move(original, target)

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y %H:%M:%S")
os.rename(f'{target}{original}', f'{target}{dt_string}')
