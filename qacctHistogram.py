import os.path, time
import datetime
import seaborn as sns
import matplotlib
import pandas as pd
import numpy as np

# Use a non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    'Log Pending Time (log10 minutes)': np.log10([x if x > 0 else 1e-10 for x in pendingTimes]),
    'Log Running Time (log10 minutes)': np.log10([x if x > 0 else 1e-10 for x in runningTimes])
})

# Customize the plot
g = sns.jointplot(x='Log Pending Time (log10 minutes)', y='Log Running Time (log10 minutes)', data=data, kind='hex', 
                  color='cyan', edgecolor='k')

# Customize the appearance to match the background
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Pending vs Running Time (Minutes Log10 transformed)', color='white')
g.set_axis_labels('Log Pending Time (log10 minutes)', 'Log Running Time (log10 minutes)', fontsize=12, color='white')

for ax in [g.ax_joint, g.ax_marg_x, g.ax_marg_y]:
    ax.tick_params(colors='white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    # Set the ticks for each power of 10
    ax.set_xticks([np.log10(x) for x in [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]])
    ax.set_xticklabels([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])
    ax.set_yticks([np.log10(x) for x in [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000]])
    ax.set_yticklabels([0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000])

g.ax_joint.patch.set_facecolor('#282a36')
g.ax_marg_x.patch.set_facecolor('#282a36')
g.ax_marg_y.patch.set_facecolor('#282a36')

# Save the figure
file_path = "/home/riano/qstat_html/pending_vs_running_time_log10.png"
g.savefig(file_path, facecolor='#282a36')