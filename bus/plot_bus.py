#!/usr/bin/env python

import datetime
import pytz
import pandas as pd
import seaborn as sns
import json
import re

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

import numpy as np

sns.set()
plt.rc('figure', figsize=(11.69, 8.27))

DATAFILE = 'transits-milton_road_2_in.csv'


mon_fri = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['Nov 2018', 'Dec',
          'Jan 2019', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

hours = ['07:30', '08:00', '08:30', '09:00', '09:30']


def get_bus_data():

    # "Date","Duration","Distance"

    df = pd.read_csv(DATAFILE)

    df.index = pd.to_datetime(df['Date'])
    df = df.sort_index()
    df.drop('Date', axis=1, inplace=True)

    df = df.resample('15min').agg({'Duration': np.mean, 'Distance': np.mean})

    df['minutes'] = df.Duration/60
    df['rounded_minutes'] = (df.index.minute//15) * 15
    df['Month'] = df.index.year * 100 + df.index.month

    return df


def setup_axies(ax, max, xlabel):

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel(xlabel)

    ax.set_ylabel('Duration (minutes)')
    ax.set_ylim([0, max])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))


def do_boxplot(df, by, column, xlabel, ymax, title, savefile, labels=[], hod=False):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df.boxplot(
        by=by,
        column=column,
        grid=False,
        # whis='range',
        ax=ax)

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel(xlabel)
    if labels:
        ax.set_xticklabels(labels)
    elif hod:
        ax.set_xticklabels(['{:02d}:{:02d}'.format(int(x.get_text()) // 100, int(x.get_text()) % 100) for x in ax.get_xticklabels()])

    ax.set_ylabel('Minutes')
    ax.set_ylim([0, ymax])
    ax.set_title(title)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    fig.suptitle('Milton Road Bus Journey Times\n(Busway to Elizabeth Way, Nov 2018-Oct 2019, 07:30-09:30)')

    plt.savefig(savefile)

    plt.close()


def do_histplot(column, bins, xmax, title, savefile):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    column.plot.hist(bins=bins, range=(0, xmax), ax=ax)

    ax.grid(axis='y')

    ax.set_ylim([0, 300])
    ax.set_xlim([0, xmax])

    print(column.max())

    ax.axvline(x=column.max(), linestyle='--')
    ax.annotate('Max', xy=(column.max() , 0.9), xycoords=('data', 'axes fraction'),
                xytext=(-30, 0), textcoords='offset points',
                ha='right', arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle="->"))

    ax.set_xlabel('Minutes')
    ax.set_title(title)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    fig.suptitle('Milton Road Bus Journey Times\n(Busway to Elizabeth Way, Nov 2018-Oct 2019, 07:30-09:30)')

    plt.savefig(savefile)

    plt.close()


df = get_bus_data()

# 07:30 - 09:30, Mon to Fri
df_sample = df[(
                 ((df.index.hour == 7) & (df.index.minute >= 30)) |
                 (df.index.hour == 8) |
                 ((df.index.hour == 9) & (df.index.minute < 30))
               ) &
               (
                 df.index.dayofweek < 5
               )]

print(df_sample.describe())

print(df_sample)

# ***** Passenger Duration

do_histplot(df_sample.minutes, 60, 15, 'All journeys', 'bus-hist.pdf')


# =============== By hour of day

YMAX = 15

do_boxplot(
    df_sample, 100*df_sample.index.hour+df_sample.rounded_minutes, 'minutes',
    'Time of Day', YMAX, 'Journeys by time of day',
    'bus-tod.pdf', hod=True)

# =============== By month of year, mon-fri 07:00-18:00

do_boxplot(
    df_sample, df_sample.Month, 'minutes',
    '', YMAX, 'Journeys by month',
    'bus-month.pdf', labels=months)

# =============== By day of week

do_boxplot(
    df_sample, df_sample.index.dayofweek, 'minutes',
    '', YMAX, 'Journeys by day of week',
    'bus-dow.pdf', labels=mon_fri)

# =============== Grand summary - Mon-Fri, 07:00-18:00

fig, ax = plt.subplots(nrows=1, ncols=1)

df_sample.boxplot(
    column='minutes',
    grid=False,
    # whis='range',
    ax=ax)

ax.set_title('')
ax.grid(axis='y')

ax.set_xticklabels([])

ax.set_ylabel('Minutes')
ax.set_ylim([0, YMAX])
ax.set_title('All journeys')
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

fig.suptitle('Milton Road Bus Journey Times\n(Busway to Elizabeth Way, Nov 2018-Oct 2019, 07:30-09:30)')

plt.savefig('bus-overall.pdf')

plt.close()
