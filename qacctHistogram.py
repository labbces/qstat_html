import os
import time
import datetime
import pandas as pd
import numpy as np
import sys
import gzip
import argparse
import seaborn as sns
import matplotlib
import json

# Use a non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process SGE accounting file and generate histogram.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the accounting file (can be .gz)')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output plot file path')
    return parser.parse_args()

def open_accounting_file(file_path):
    return gzip.open(file_path, 'rt') if file_path.endswith('.gz') else open(file_path, 'r')

def file_age_in_days(file_path):
    last_mod = datetime.datetime.strptime(time.ctime(os.path.getmtime(file_path)), "%a %b %d %H:%M:%S %Y")
    now = datetime.datetime.now()
    return (now - last_mod) / datetime.timedelta(days=1)

def parse_accounting_file(file_path):
    job_records = []
    current_job = {'qsub_time': None, 'start_time': None, 'end_time': None}

    with open_accounting_file(file_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith('qsub_time'):
                current_job['qsub_time'] = line.split('qsub_time')[-1].strip()
            elif line.startswith('start_time'):
                current_job['start_time'] = line.split('start_time')[-1].strip()
            elif line.startswith('end_time'):
                current_job['end_time'] = line.split('end_time')[-1].strip()
            elif line.startswith('=============================================================='):
                if all(current_job.values()) and '-/-' not in current_job.values():
                    job_records.append(current_job.copy())
                current_job = {'qsub_time': None, 'start_time': None, 'end_time': None}

    return pd.DataFrame(job_records)

def process_job_dataframe(df):
    if df.empty:
        print('No valid jobs found.')
        return None

    df['qsub_time'] = pd.to_datetime(df['qsub_time'], format='%a %b %d %H:%M:%S %Y')
    df['start_time'] = pd.to_datetime(df['start_time'], format='%a %b %d %H:%M:%S %Y')
    df['end_time'] = pd.to_datetime(df['end_time'], format='%a %b %d %H:%M:%S %Y')

    df['pending_time_min'] = (df['start_time'] - df['qsub_time']).dt.total_seconds() / 60
    df['running_time_min'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60

    df = df[(df['pending_time_min'] >= 0) & (df['running_time_min'] >= 0)]

    return df

def generate_histogram(df, histogram_plot):
    data = pd.DataFrame({
        'Log Pending Time (log10 minutes)': np.log10(df['pending_time_min'].replace(0, 1e-10)),
        'Log Running Time (log10 minutes)': np.log10(df['running_time_min'].replace(0, 1e-10))
    })

    g = sns.jointplot(x='Log Pending Time (log10 minutes)', y='Log Running Time (log10 minutes)', data=data, kind='hex',
                      color='red', edgecolor='k')

    plt.subplots_adjust(top=0.9)
    g.fig.suptitle('Pending vs Running Time Minutes (Log10)', color='white')
    g.set_axis_labels('Pending Time (minutes)', 'Running Time (minutes)', fontsize=12, color='white')

    for ax in [g.ax_joint, g.ax_marg_x, g.ax_marg_y]:
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')

        powers_of_ten = range(-10, 6)
        ax.set_xticks(powers_of_ten)
        ax.set_xticklabels(['$10^{{{}}}$'.format(p) for p in powers_of_ten])
        ax.set_yticks(powers_of_ten)
        ax.set_yticklabels(['$10^{{{}}}$'.format(p) for p in powers_of_ten])

    g.ax_joint.set_xlim(np.log10(1e-2), np.log10(1e5))
    g.ax_joint.set_ylim(np.log10(1e-10), np.log10(1e5))

    g.ax_joint.patch.set_facecolor('#282a36')
    g.ax_marg_x.patch.set_facecolor('#282a36')
    g.ax_marg_y.patch.set_facecolor('#282a36')

    for label in g.ax_joint.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    g.ax_marg_y.hist(data['Log Running Time (log10 minutes)'], bins=60, orientation='horizontal', color='red', edgecolor='k')

    g.savefig(histogram_plot, facecolor='#282a36')
    print(f'Histogram saved to {histogram_plot}')

if __name__ == '__main__':
    args = parse_arguments()

    if not os.path.exists(args.file):
        print(f'Error: The file {args.file} does not exist.')
        sys.exit(1)

    file_age = file_age_in_days(args.file)

    if file_age > 60:
        print(f'File {args.file} was modified {file_age:.2f} days ago. You should regenerate it with:')
        print(f'qacct -j "*" > {args.file}')
        sys.exit(0)

    regenerate_plot = True

    if os.path.exists(args.output):
        plot_age = file_age_in_days(args.output)
        if plot_age < 30:
            print(f'Plot {args.output} is up-to-date (modified {plot_age:.2f} days ago). Nothing to do.')
            regenerate_plot = False
        else:
            print(f'Plot {args.output} is older than 30 days. Regenerating.')

    if regenerate_plot:
        df = parse_accounting_file(args.file)
        df = process_job_dataframe(df)
        if df is not None and not df.empty:
            print(df[['pending_time_min', 'running_time_min']].describe())
            generate_histogram(df, args.output)
            with open("summary_stats.json", "w") as f:
                json.dump(df[['pending_time_min', 'running_time_min']].describe().to_dict(), f, indent=2)
        else:
            print('No valid durations found.')

