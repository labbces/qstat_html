import os.path, time
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

accFile='/home/riano/qstat_html/qAccounting.txt'
lastMod=datetime.datetime.strptime(time.ctime(os.path.getmtime(accFile)), "%a %b %d %H:%M:%S %Y")
now=datetime.datetime.now()

differenceTime = now - lastMod
print(differenceTime)

pendingTimes=[]
runningTimes=[]
submitTime=0
countJobs=0

with open(accFile) as f:
    for line in f:
        line=line.strip()
        if line.startswith('qsub_time'):
            submitTime=line.replace('qsub_time    ', '')
        elif line.startswith('start_time'):
            startTime=line.replace('start_time   ', '')
        elif line.startswith('end_time'):
            endTime=line.replace('end_time     ', '')
        elif line.startswith('=============================================================='):
            countJobs+=1
            #print a progress bar
            if countJobs % 1000 == 0:
                print(f'{countJobs} jobs processed', flush=True)
            if (submitTime != 0):
                if submitTime == '-/-' or startTime == '-/-' or endTime == '-/-':
                    #print("Error in the accounting file")
                    submitTime=0
                    startTime=0
                    endTime=0
                else:
                    pendingTime=datetime.datetime.strptime(startTime, "%a %b %d %H:%M:%S %Y")-datetime.datetime.strptime(submitTime, "%a %b %d %H:%M:%S %Y")
                    runnnigTime=datetime.datetime.strptime(endTime, "%a %b %d %H:%M:%S %Y")-datetime.datetime.strptime(startTime, "%a %b %d %H:%M:%S %Y")
                    pendingTime_inMinutes=pendingTime / datetime.timedelta(minutes=1)
                    runnnigTime_inMinutes=runnnigTime / datetime.timedelta(minutes=1)
#                    print(f'submit Time:\t{submitTime}\nstart Time:\t{startTime}\nend Time:\t{endTime}\nPending Time:\t{pendingTime_inMinutes}\nRunning Time:\t{runnnigTime_inMinutes}', flush=True)
                    pendingTimes.append(pendingTime_inMinutes)
                    runningTimes.append(runnnigTime_inMinutes)
                    submitTime=0
                    startTime=0
                    endTime=0

# Create a DataFrame from the data
data = pd.DataFrame({
    'Pending Time (minutes)': pendingTimes,
    'Running Time (minutes)': runningTimes
})

# Plot the 2D histogram and its 1D projections
g = sns.jointplot(x='Pending Time (minutes)', y='Running Time (minutes)', data=data, kind='hex')

# Save the figure
g.savefig("jointplot_histogram.png")