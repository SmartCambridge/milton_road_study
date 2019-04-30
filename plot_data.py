#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set()
plt.rc('figure', figsize=(11.69, 8.27))

plots = [
    {'zone': 'milton_pandr_south',
     'max': 2700
     },
    {'zone': 'milton_pandr_north',
     'max': 2700
     },
]

def setup_axies(ax, max):

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel('Day of Year')

    ax.set_ylabel('Duration (sec)')
    ax.set_ylim([0, max])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(300))


for plot in plots:

    basename = 'transits-{}'.format(plot['zone'])

    df = pd.read_csv(basename + '.csv', delimiter=',')

    # Set index from 'Date' column and delete it
    df['Date'] = pd.to_datetime(df['Date'])
    df.index = df['Date']
    df.index = df.index.tz_convert('Europe/London')
    del df['Date']

    # Drop records with Duration below 0.5'th percentile or above 99.5'th
    df = df[(df.Duration > df.Duration.quantile(.005)) &
            (df.Duration < df.Duration.quantile(.995))]

    df_weekdays = df[df.index.dayofweek < 5]
    df_weekends = df[df.index.dayofweek >= 5]

    # =============== Weekdays, by day of year

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df_weekdays.boxplot(
        by=df_weekdays.index.dayofyear,
        column=['Duration'],
        grid=False,
        whis='range',
        ax=ax)

    setup_axies(ax, plot['max'])
    ax.set_xlabel('Day of Year')
    fig.suptitle('{} by day (weekdays)'.format(plot['zone']))

    plt.savefig(basename + '-mon-fri.pdf')

    plt.close()

    # =============== Weekdays, by month of year

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df_weekdays.boxplot(
        by=df_weekdays.index.month,
        column=['Duration'],
        grid=False,
        whis='range',
        ax=ax)

    setup_axies(ax, plot['max'])
    ax.set_xlabel('Month of Year')
    fig.suptitle('{} by month (weekdays)'.format(plot['zone']))

    plt.savefig(basename + '-mon-fri-month.pdf')

    plt.close()

    # =============== Weekends, by day of year

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df_weekends.boxplot(
        by=df_weekends.index.dayofyear,
        column=['Duration'],
        grid=False,
        whis='range',
        ax=ax)

    setup_axies(ax, plot['max'])
    ax.set_xlabel('Day of Year')
    fig.suptitle('{} by day (weekends)'.format(plot['zone']))

    plt.savefig(basename + '-sat-sun.pdf')

    plt.close()

    # =============== By day of week

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df.boxplot(
        by=df.index.dayofweek,
        column=['Duration'],
        grid=False,
        whis='range',
        ax=ax)

    setup_axies(ax, plot['max'])
    ax.set_xlabel('Day of week (0 = Monday)')
    fig.suptitle('{} by day of week'.format(plot['zone']))

    plt.savefig(basename + '-dow.pdf')

    plt.close()

    # =============== By hour of day, weekdays

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df_weekdays.boxplot(
        by=df_weekdays.index.hour,
        column=['Duration'],
        grid=False,
        whis='range',
        ax=ax)

    setup_axies(ax, plot['max'])
    ax.set_xlabel('Hour of the day')
    fig.suptitle('{} by hour of day (weekdays)'.format(plot['zone']))

    plt.savefig(basename + 'mon-fri-hod.pdf')

    plt.close()

    # =============== By hour of day, weekends

    fig, ax = plt.subplots(nrows=1, ncols=1)

    df_weekends.boxplot(
        by=df_weekends.index.hour,
        column=['Duration'],
        grid=False,
        whis='range',
        ax=ax)

    setup_axies(ax, plot['max'])
    ax.set_xlabel('Hour of the day')
    fig.suptitle('{} by hour of day (weekends)'.format(plot['zone']))

    plt.savefig(basename + 'sat-sun-hod.pdf')

    plt.close()
