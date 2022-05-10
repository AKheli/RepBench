import datetime
""" add output to txt file of things are logged some code including the asserts are skipped"""

now = datetime.datetime.now()
file_name = "log_" + now.strftime("%d %H:%M")+".txt"
do_log =True

def add_to_log(txt):
    with open(file_name, 'a') as f:
        f.f.write(txt)
        f.write('\n')