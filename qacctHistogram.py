import os.path, time
import datetime

accFile='/home/riano/qstat_html/qAccounting.txt'
lastMod=datetime.datetime.strptime(time.ctime(os.path.getmtime(accFile)), "%a %b %d %H:%M:%S %Y")
now=datetime.datetime.now()

differenceTime = now - lastMod
print(differenceTime)

pendingTimes=[]
runningtimes=[]
submitTime=0

with open(accFile) as f:
    for line in f:
        if line.startswith('qsub_time'):
            submitTime=line.split()[1]
        elif line.startswith('start_time'):
            startTime=line.split()[1]
        elif line.startswith('end_time'):
            endTime=line.split()[1]
        elif line.startswith('=============================================================='):
            print(line)
            if (submitTime != 0):
                pendingTime=datetime.datetime.strptime(startTime, "%a %b %d %H:%M:%S %Y")-datetime.datetime.strptime(submitTime, "%a %b %d %H:%M:%S %Y")
                runnnigTime=datetime.datetime.strptime(endTime, "%a %b %d %H:%M:%S %Y")-datetime.datetime.strptime(startTime, "%a %b %d %H:%M:%S %Y")
                print(f'submit Time:\t{submitTime}\nstart Time:\t{startTime}\nend Time:\t{endTime}\nPending Time:\t{pendingTime}\nRunning Time:\t{runnnigTime}', flush=True)
                pendingTimes.append(pendingTime)
                runningtimes.append(runnnigTime)
                submitTime=0
                startTime=0
                endTime=0