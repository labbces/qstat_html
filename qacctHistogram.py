import os.path, time
import datetime
import seaborn as sns
import matplotlib
import pandas as pd
import numpy as np
import sys

# Use a non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt

accFile='/home/riano/qstat_html/qAccounting.txt'
histogramPlot = "/home/riano/qstat_html/pending_vs_running_time_log10.png"

lastMod=datetime.datetime.strptime(time.ctime(os.path.getmtime(accFile)), "%a %b %d %H:%M:%S %Y")
now=datetime.datetime.now()

differenceTime = now - lastMod
differenceTime_inDays = differenceTime / datetime.timedelta(days=1)

def generateHistrogram(accFile, histogramPlot):
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
                if countJobs % 10000 == 0:
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
                    color='red', edgecolor='k')

    # Customize the appearance to match the background
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle('Pending vs Running Time Minutes (Log10 transformed)', color='white')
    g.set_axis_labels('Pending Time (minutes)', 'Running Time (minutes)', fontsize=12, color='white')

    for ax in [g.ax_joint, g.ax_marg_x, g.ax_marg_y]:
        ax.tick_params(colors='white')
        ax.spines['left'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        # Set the ticks for each power of 10
        powers_of_ten = np.log10(np.logspace(-10, 5, num=16))
        ax.set_xticks(powers_of_ten)
        ax.set_xticklabels(['$10^{{{:.0f}}}$'.format(p) for p in range(-10, 6)])
        ax.set_yticks(powers_of_ten)
        ax.set_yticklabels(['$10^{{{:.0f}}}$'.format(p) for p in range(-10, 6)])

    # Set limits for the axes
    g.ax_joint.set_xlim(np.log10(1e-2), np.log10(1e5))
    g.ax_joint.set_ylim(np.log10(1e-10), np.log10(1e5))

    g.ax_joint.patch.set_facecolor('#282a36')
    g.ax_marg_x.patch.set_facecolor('#282a36')
    g.ax_marg_y.patch.set_facecolor('#282a36')

    # Rotate x-axis labels for better readability
    for label in g.ax_joint.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    # Change the color of the 1D histogram bars
    #g.ax_marg_x.hist(data['Log Pending Time (log10 minutes)'], bins=60, color='#1632e7', edgecolor='k')
    g.ax_marg_y.hist(data['Log Running Time (log10 minutes)'], bins=60, orientation='horizontal', color='red', edgecolor='k')

    # Save the figure
    g.savefig(histogramPlot, facecolor='#282a36')

if differenceTime_inDays > 60:
    print(f'File was modified {differenceTime_inDays} days ago. You should generate again the file {accFile}', flush=True)
    print(f'To do that run qacct -j "*" > {accFile}', flush=True)
    print(f'Exiting the program', flush=True)
    sys.exit()
else:
    if os.path.exists(histogramPlot):
        print(f'File {histogramPlot} already exists. Nothing to do here.', flush=True)
    else:
        generateHistrogram(accFile, histogramPlot)