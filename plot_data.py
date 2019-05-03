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

    column.plot.hist(bins=bins, range=(0, xmax), ax=ax)

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
    df_valid_intervals = df[(df.Interval_minutes < 60)]
    df_weekday_intervals = df[(df.Interval_minutes < 60) & (df.index.dayofweek < 5)]
    df_weekend_intervals = df[(df.Interval_minutes < 60) & (df.index.dayofweek >= 5)]
    # Subset in on or after 07:00, before 18:00 when timetabled interval in 10 min
    df_valid_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.hour >= 7) & (df.index.hour < 18)]
    df_weekday_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.hour >= 7) & (df.index.hour < 18) & (df.index.dayofweek < 5)]
    df_weekend_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.hour >= 7) & (df.index.hour < 18) & (df.index.dayofweek >= 5)]

    # ***** Trip Duration

    do_histplot(
        df.Duration_minutes, 30, 30, plot['zone'], 'all trip durations',
        basename + '-all_trip-hist.pdf')

    # =============== By hour of day, mon-fri

    do_boxplot(
        df_weekdays, df_weekdays.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all trip durations, by hour of day (Mon-Fri)',
        basename + '-all_trip-hod-mon_fri.pdf')

    # =============== By hour of day, sat-sun

    do_boxplot(
        df_weekends, df_weekends.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all trip durations, by hour of day (Sat-Sun)',
        basename + '-all_trip-hod-sat_sun.pdf')

    # =============== By month of year, mon-fri

    do_boxplot(
        df_weekdays, df_weekdays.index.month, 'Duration_minutes',
        'Month of year', plot['zone'], plot['max'], 'all trip durations, by month of year (Mon-Fri)',
        basename + '-all_trip-moy-mon_fri.pdf')

    # =============== By month of year, sat-sun

    do_boxplot(
        df_weekends, df_weekends.index.month, 'Duration_minutes',
        'Month of Year', plot['zone'], plot['max'], 'all trip durations, by month of year (Sat-Sun)',
        basename + '-all_trip-moy-sat_sun.pdf')

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'Duration_minutes',
        'Day of Week (0 = Monday)', plot['zone'], plot['max'], 'all trip durations, by day of week',
        basename + '-all_trip-dow.pdf')

    # ***** Service interval

    do_histplot(
        df_valid_intervals.Interval_minutes, 60, 60, plot['zone'], 'all service intervals',
        basename + '-interval-hist.pdf')

    # =============== By hour of day, mon-fri

    do_boxplot(
        df_weekday_intervals, df_weekday_intervals.index.hour, 'Interval_minutes',
        'Hour of day', plot['zone'], plot['max'], 'all service intervals, by hour of day (Mon-Fri)',
        basename + '-interval-hod-mon_fri.pdf')

    # =============== By hour of day, weekdays

    do_boxplot(
        df_weekend_intervals, df_weekend_intervals.index.hour, 'Interval_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all service intervals, by hour of day (Sat-Sun)',
        basename + '-interval-hod-sat_sun.pdf')

    # =============== By month of year, mon-fri

    do_boxplot(
        df_weekday_intervals_subset, df_weekday_intervals_subset.index.month, 'Interval_minutes',
        'Month of year', plot['zone'], plot['max'], 'service intervals, by month of year (Mon-Fri, 07:00-18:00)',
        basename + '-interval-moy-mon_fri.pdf')

    # =============== By month of year, weekdays

    do_boxplot(
        df_weekend_intervals_subset, df_weekend_intervals_subset.index.hour, 'Interval_minutes',
        'Month of year', plot['zone'], plot['max'], 'all service intervals, by month of year (Sat-Sun, 07:00-18:00)',
        basename + '-interval-moy-sat_sun.pdf')

    # =============== By day of week

    do_boxplot(
        df_valid_intervals_subset, df_valid_intervals_subset.index.dayofweek, 'Interval_minutes',
        'Day of Week (0 = Monday)', plot['zone'], plot['max'], 'all service intervals, by day of week (07:00-18:00)',
        basename + '-interval-dow.pdf')

    # # == Worst case

    do_histplot(
        df_valid_intervals.Worst_case, 100, 100, plot['zone'], 'worst trip duration',
        basename + '-worst-hist.pdf')

    # =============== Sample, best/worst by month of day

    do_boxplot(
        df_weekday_intervals_subset, df_weekday_intervals_subset.index.month, 'Worst_case',
        'Month of Year', plot['zone'], plot['max'], 'worst trip duration, by month (Mon-Fri, 07:00-18:00)',
        basename + '-worst-moy.pdf')

    # =============== Sample, best/worst by hour of day

    do_boxplot(
        df_weekday_intervals, df_weekday_intervals.index.hour, 'Worst_case',
        'Hour of Day', plot['zone'], plot['max'], 'worst trip duration, by hour of day (Mon-Fri)',
        basename + '-worst-hod.pdf')

    # =============== Sample,best/worst by day of week

    do_boxplot(
        df_valid_intervals_subset, df_valid_intervals_subset.index.dayofweek, 'Worst_case',
        'Day of Week (0 = Monday)', plot['zone'], plot['max'], 'worst trip duration, by day of week (Mon-Fri, 07:00-18:00)',
        basename + '-worst-dow.pdf')

    # Best/Worst compared

    best_sum = df_weekday_intervals_subset.Duration_minutes.groupby(df_weekday_intervals_subset.index.hour).quantile(0.75)
    worst_sum = df_weekday_intervals_subset.Worst_case.groupby(df_weekday_intervals_subset.index.hour).quantile(0.75)

    df_plot = pd.concat([best_sum, worst_sum], axis = 1)

    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.bar(df_plot.index, df_plot.Worst_case, bottom=df_plot.Duration_minutes, fill=False, edgecolor=['b'])
    ax.grid(axis='x')
    ax.set_ylim([0, plot['max']])
    ax.set_xlabel('Hour of day')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    fig.suptitle('{} {}'.format(plot['zone'], 'Best and worst journeys, 75\'th percentile (Mon-Fri, 07:00 - 18:00)'))
    plt.savefig(basename + '-best_worst.pdf')
    plt.close()
