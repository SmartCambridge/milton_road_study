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

DATAFILES = [
    'drakewell_data/2018-08.csv',
    'drakewell_data/2018-09.csv',
    'drakewell_data/2018-10.csv',
    'drakewell_data/2018-11.csv',
    'drakewell_data/2018-12.csv',
    'drakewell_data/2019-01.csv',
    'drakewell_data/2019-02.csv',
    'drakewell_data/2019-03.csv',
    'drakewell_data/2019-04.csv',
    'drakewell_data/2019-05.csv',
    'drakewell_data/2019-06.csv',
    'drakewell_data/2019-07.csv',
    'drakewell_data/2019-08.csv',
    'drakewell_data/2019-09.csv',
    'drakewell_data/2019-10.csv',
]

COSIT = '9800XCZR4LWP'


sns.set()
plt.rc('figure', figsize=(11.69, 8.27))


mon_fri = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['Aug 2018', 'Sep', 'Oct', 'Nov', 'Dec',
          'Jan 2019', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']


def get_drakewell_data():

    global links, sites

    # Slurp link and site details
    with open('locations.json') as f:
        locations = json.load(f)
    links = {re.sub(r'CAMBRIDGE_JTMS\|', '', record['id']): record for record in locations['links']}
    sites = {record['id']: record for record in locations['sites']}

    df = pd.concat(map(pd.read_csv, DATAFILES))
    df.columns = ['node', 'cosit', 'timestamp', 'period', 'seconds', 'count']
    df['minutes'] = df.seconds/60
    df.index = pd.to_datetime(df['timestamp'])
    df.index = df.index.tz_localize('Europe/London', ambiguous='NaT')
    df = df.sort_index()

    df['Month'] = df.index.year * 100 + df.index.month

    df.drop('timestamp', axis=1, inplace=True)

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
        whis='range',
        ax=ax)

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel(xlabel)
    if labels:
        ax.set_xticklabels(labels)
    elif hod:
        ax.set_xticklabels(['{:02d}'.format(int(x.get_text())) for x in ax.get_xticklabels()])

    ax.set_ylabel('Minutes')
    ax.set_ylim([0, ymax])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    fig.suptitle('A14/Milton Rd to Lensfield Rd/Trumpington St. ' + title)

    plt.savefig(savefile)

    plt.close()


def do_histplot(column, bins, xmax, title, savefile):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    column.plot.hist(bins=bins, range=(0, xmax), ax=ax)

    ax.grid(axis='y')

    ax.set_ylim([0, 5000])

    ax.set_xlabel('Minutes')

    fig.suptitle('A14/Milton Rd to Lensfield Rd/Trumpington St. ' + title)

    plt.savefig(savefile)

    plt.close()


df = get_drakewell_data()

df['Month'] = df.index.year * 100 + df.index.month

# Some filtered data frames
df_7_to_18 = df[(df.index.hour >= 7) & (df.index.hour < 18)]
df_weekdays = df[df.index.dayofweek < 5]
df_weekdays_7_to_18 = df[(df.index.dayofweek < 5) & (df.index.hour >= 7) & (df.index.hour < 18)]
df_saturday = df[df.index.dayofweek == 5]
df_saturday_8_to_18 = df[(df.index.dayofweek == 5) & (df.index.hour >= 8) & (df.index.hour < 18)]
df_sunday = df[df.index.dayofweek == 6]

# ***** Passenger Duration

do_histplot(df.minutes, 100, 100, 'all journeys', 'drakewell-hist.pdf')

# =============== By hour of day, mon-fri

YMAX = 100

do_boxplot(
    df_weekdays, df_weekdays.index.hour, 'minutes',
    'Hour of Day', YMAX, 'all journeys, by hour of day (Mon-Fri)',
    'drakewell-hod-mon_fri.pdf', hod=True)

# =============== By hour of day, sat

do_boxplot(
    df_saturday, df_saturday.index.hour, 'minutes',
    'Hour of Day', YMAX, 'all journeys, by hour of day (Sat)',
    'drakewell-hod-sat.pdf', hod=True)

# =============== By hour of day, sun

do_boxplot(
    df_sunday, df_sunday.index.hour, 'minutes',
    'Hour of Day', YMAX, 'all journeys, by hour of day (Sun)',
    'drakewell-hod-sun.pdf', hod=True)

# =============== By month of year, mon-fri 07:00-18:00

do_boxplot(
    df_weekdays_7_to_18, df_weekdays_7_to_18.Month, 'minutes',
    '', YMAX, 'journeys, by month of year (Mon-Fri, 07:00-18:00)',
    'drakewell-moy-mon_fri.pdf', labels=months)

# =============== By month of year, Sat 08:00-18:00

do_boxplot(
    df_saturday_8_to_18, df_saturday_8_to_18.Month, 'minutes',
    '', YMAX, 'journeys, by month of year (Sat, 08:00-18:00)',
    'drakewell-moy-sat.pdf', labels=months)

# =============== By month of year, Sun

do_boxplot(
    df_sunday, df_sunday.Month, 'minutes',
    '', YMAX, 'journeys, by month of year (Sun)',
    'drakewell-moy-sun.pdf', labels=months)

# =============== By day of week

do_boxplot(
    df_7_to_18, df_7_to_18.index.dayofweek, 'minutes',
    '', YMAX, 'journeys, by day of week (07:00-18:00)',
    'drakewell-dow.pdf', labels=mon_fri)

# =============== Example daily graph

fig, ax = plt.subplots(nrows=1, ncols=1)

df['2019-04-02'].minutes.plot(style='b.', ax=ax)

ax.grid(axis='y')

ax.set_ylim([0, 40])

ax.set_xlabel('')
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M', tz=pytz.timezone('Europe/London')))
ax.set_xlim([datetime.datetime(2019, 4, 2, 0), datetime.datetime(2019, 4, 3, 0)])
ax.set_ylabel('Minutes')

fig.suptitle('Example journey time (2019-04-02)')

plt.savefig('drakewell-example.pdf')

plt.close()

# =============== Grand summary - Mon-Fri, 07:00-18:00

fig, ax = plt.subplots(nrows=1, ncols=1)

df_7_to_18.boxplot(
    column='minutes',
    grid=False,
    whis='range',
    ax=ax)

ax.set_title('')
ax.grid(axis='y')

ax.set_xticklabels([])

ax.set_ylabel('Minutes')
ax.set_ylim([0, YMAX])
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

fig.suptitle('all journeys (Mon-Fri, 07:00-18:00)')

plt.savefig('drakewell-overall.pdf')

plt.close()
