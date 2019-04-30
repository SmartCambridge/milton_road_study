#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set()
plt.rc('figure', figsize=(11.69, 8.27))

plots = [
    {'years': [2018, 2019],
     'zone': 'a428_east',
     'max': 2500
     },
    {'years': [2018, 2019],
     'zone': 'a428_west',
     'max': 2500
     },
    {'years': [2019],
     'zone': 'a428_caxton_east',
     'max': 1500
     },
    {'years': [2019],
     'zone': 'a428_caxton_west',
     'max': 1500
     },
    {'years': [2018, 2019],
     'zone': 'a1m_north',
     'max': 600
     },
    {'years': [2018, 2019],
     'zone': 'a1m_south',
     'max': 600
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

    for year in plot['years']:

        basename = 'transits-{}-{}'.format(plot['zone'], year)

        df = pd.read_csv(basename + '.csv', delimiter=',')

        # Set index from 'Date' column and delete it
        df['Date'] = pd.to_datetime(df['Date'])
        df.index = df['Date']
        df.index = df.index.tz_convert('Europe/London')
        del df['Date']

        # Drop records with Duration below 0.5'th percentile or above 99.5'th
        df = df[(df.Duration > df.Duration.quantile(.005)) &
                (df.Duration < df.Duration.quantile(.995))]

        # =============== Weekdays, by day of year

        df_weekdays = df[df.index.dayofweek < 5]

        fig, ax = plt.subplots(nrows=1, ncols=1)

        df_weekdays.boxplot(
            by=df_weekdays.index.dayofyear,
            column=['Duration'],
            grid=False,
            whis='range',
            ax=ax)

        setup_axies(ax, plot['max'])
        ax.set_xlabel('Day of Year')
        fig.suptitle('{} {} by day (weekdays)'.format(plot['zone'], year))

        plt.savefig(basename + '-mon-fri.pdf')

        plt.close()

        # =============== Weekdays, by month of year

        df_weekdays = df[df.index.dayofweek < 5]

        fig, ax = plt.subplots(nrows=1, ncols=1)

        df_weekdays.boxplot(
            by=df_weekdays.index.month,
            column=['Duration'],
            grid=False,
            whis='range',
            ax=ax)

        setup_axies(ax, plot['max'])
        ax.set_xlabel('Month of Year')
        fig.suptitle('{} {} by month (weekdays)'.format(plot['zone'], year))

        plt.savefig(basename + '-month.pdf')

        plt.close()

        # =============== Weekends, by day of year

        df_weekends = df[df.index.dayofweek >= 5]

        fig, ax = plt.subplots(nrows=1, ncols=1)

        df_weekends.boxplot(
            by=df_weekends.index.dayofyear,
            column=['Duration'],
            grid=False,
            whis='range',
            ax=ax)

        setup_axies(ax, plot['max'])
        ax.set_xlabel('Day of Year')
        fig.suptitle('{} {} by day (weekends)'.format(plot['zone'], year))

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
        fig.suptitle('{} {} by day of week'.format(plot['zone'], year))

        plt.savefig(basename + '-dow.pdf')

        plt.close()

        # =============== By hour of day

        fig, ax = plt.subplots(nrows=1, ncols=1)

        df.boxplot(
            by=df.index.hour,
            column=['Duration'],
            grid=False,
            whis='range',
            ax=ax)

        setup_axies(ax, plot['max'])
        ax.set_xlabel('Hour of the day')
        fig.suptitle('{} {} by hour of day'.format(plot['zone'], year))

        plt.savefig(basename + '-hod.pdf')

        plt.close()
