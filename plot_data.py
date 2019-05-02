#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set()
plt.rc('figure', figsize=(11.69, 8.27))

plots = [
    {'zone': 'milton_pandr_south',
     'max': 100
     },
    {'zone': 'milton_pandr_north',
     'max': 100
     },
]


def setup_axies(ax, max, xlabel):

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel(xlabel)

    ax.set_ylabel('Duration (minutes)')
    ax.set_ylim([0, max])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))


def do_boxplot(df, by, column, xlabel, zone, ymax, title, savefile):

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

    ax.set_ylabel('Minutes')
    ax.set_ylim([0, ymax])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    fig.suptitle('{} {}'.format(zone, title))

    plt.savefig(savefile)

    plt.close()


def do_histplot(column, bins, xmax, zone, title, savefile):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    column.plot.hist(bins=bins, range=(0,xmax))

    ax.grid(axis='y')

    ax.set_xlabel('Minutes')

    fig.suptitle('{} {}'.format(zone, title))

    plt.savefig(savefile)

    plt.close()


for plot in plots:

    basename = 'transits-{}'.format(plot['zone'])

    df = pd.read_csv(basename + '.csv', delimiter=',')

    # Create some new columns

    df['Arival_timestamp'] = pd.to_datetime(df['Date'])
    del df['Date']

    df['Duration_delta'] = pd.to_timedelta(df.Duration, unit='S')
    df['Duration_minutes'] = df.Duration_delta.dt.total_seconds()/60

    df['Departure_timestamp'] = df['Arival_timestamp'] - df['Duration_delta']
    df.index = df['Departure_timestamp']
    df.index = df.index.tz_convert('Europe/London')
    df = df.sort_index()

    df['Interval_delta'] = df.Departure_timestamp.diff()
    df['Interval_minutes'] = df.Interval_delta.dt.total_seconds()/60

    df['Worst_case'] = df.Interval_minutes + df.Duration_minutes

    # Drop records with Duration below 0.5'th percentile or above 99.5'th
    df = df[(df.Duration > df.Duration.quantile(.005)) &
            (df.Duration < df.Duration.quantile(.995))]

    # Some filtered data frames
    df_weekdays = df[df.index.dayofweek < 5]
    df_weekends = df[df.index.dayofweek >= 5]
    df_intervals = df[(df.Interval_minutes < 60) & (df.index.hour >= 7) & (df.index.hour < 18) & (df.index.dayofweek < 5)]

    # # == Trip Duration

    do_histplot(
        df.Duration_minutes, 30, 30, plot['zone'], 'best trip durations',
        basename + '-best-hist.pdf')

    # =============== Weekends, by day of year

    do_boxplot(
        df_weekends, df_weekends.index.dayofyear, 'Duration_minutes',
        'Day of Year', plot['zone'], plot['max'], 'best trip duration by day (weekends)',
        basename + '-best-sat-sun-day.pdf')

    # =============== By hour of day, weekdays

    do_boxplot(
        df_weekdays, df_weekdays.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'best trip duration by hour of day (weekdays)',
        basename + '-best-mon-fri-hod.pdf')

    # =============== By hour of day, weekends

    do_boxplot(
        df_weekends, df_weekends.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'best trip duration by hour of day (weekends)',
        basename + '-best-sat-sun-hod.pdf')

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'Duration_minutes',
        'Day of Week (0 = Monday)', plot['zone'], plot['max'], 'best trip duration by day of week',
        basename + '-best-dow.pdf')

    # # == Service interval

    do_histplot(
        df_intervals.Interval_minutes, 60, 60, plot['zone'], 'service interval',
        basename + '-interval-hist.pdf')

    # =============== Weekdays, by month of year

    do_boxplot(
        df_intervals, df_intervals.index.month, 'Interval_minutes',
        'Month of Year', plot['zone'], plot['max'], 'service interval by month',
        basename + '-interval-month.pdf')

    # =============== By hour of day, weekdays

    do_boxplot(
        df_intervals, df_intervals.index.hour, 'Interval_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'service interval by hour of day',
        basename + '-interval-hod.pdf')

    # =============== By day of week

    do_boxplot(
        df_intervals, df_intervals.index.dayofweek, 'Interval_minutes',
        'Day of Week (0 = Monday)', plot['zone'], plot['max'], 'service interval by day of week',
        basename + '-interval-dow.pdf')

    # # == Worst case

    do_histplot(
        df_intervals.Worst_case, 100, 100, plot['zone'], 'worst trip duration',
        basename + '-worst-hist.pdf')

    # =============== Weekdays, by month of year

    do_boxplot(
        df_intervals, df_intervals.index.month, 'Worst_case',
        'Month of Year', plot['zone'], plot['max'], 'worst trip duration by month',
        basename + '-worst-month.pdf')

    # =============== By hour of day, weekdays

    do_boxplot(
        df_intervals, df_intervals.index.hour, 'Worst_case',
        'Hour of Day', plot['zone'], plot['max'], 'worst trip duration by hour of day',
        basename + '-worst-hod.pdf')

    # =============== By day of week

    do_boxplot(
        df_intervals, df_intervals.index.dayofweek, 'Worst_case',
        'Day of Week (0 = Monday)', plot['zone'], plot['max'], 'worst trip duration by day of week',
        basename + '-worst-dow.pdf')
