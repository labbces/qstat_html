import os.path, time
import datetime

accFile='/home/riano/qstat_html/qAccounting.txt'
lastMod=datetime.datetime.strptime(time.ctime(os.path.getmtime(accFile)), "%a %b %d %H:%M:%S %Y")
now=datetime.datetime.now()

differenceTime = now - lastMod
print(differenceTime)

pendingTimes=[]
runningtimes=[]

with open(accFile) as f:
    lines = f.readlines()
    for line in lines:
        if line.startswith('qsub_time'):
            submitTime=line.split()[1]
        elif line.startswith('start_time'):
            startTime=line.split()[1]
        elif line.startswith('end_time'):
            endTime=line.split()[1]
        elif line.startswith('=============================================================='):
            print(line)
            pendingTime=datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")-datetime.datetime.strptime(submitTime, "%Y-%m-%dT%H:%M:%S")
            runnnigTime=datetime.datetime.strptime(endTime, "%Y-%m-%dT%H:%M:%S")-datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S")
            print(f'submit Time:\t{submitTime}\nstart Time:\t{startTime}\nend Time:\t{endTime}\nPending Time:\t{pendingTime}\nRunning Time:\t{runnnigTime}')
            pendingTimes.append(pendingTime)
            runningtimes.append(runnnigTime)
            submitTime=0
            startTime=0
            endTime=0