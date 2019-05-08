#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set()
plt.rc('figure', figsize=(11.69, 8.27))

plots = [
    {'zone': 'milton_pandr_south',
     'max': 100,
     'duration': 16,
     'interval': 10,
     'sun-interval': 15
     },
    {'zone': 'milton_pandr_north',
     'max': 100,
     'duration': 20,
     'interval': 10,
     'sun-interval': 15
     },
]

mon_fri = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['Jan 2018', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
          'Jan 2019', 'Feb', 'Mar', 'Apr']


def setup_axies(ax, max, xlabel):

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel(xlabel)

    ax.set_ylabel('Duration (minutes)')
    ax.set_ylim([0, max])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))


def do_boxplot(df, by, column, xlabel, zone, ymax, title, savefile, labels=[], hod=False, hlines=[]):

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

    for hline in hlines:
        ax.axhline(hline).set_color('r')

    ax.set_ylabel('Minutes')
    ax.set_ylim([0, ymax])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    fig.suptitle('{} {}'.format(zone, title))

    plt.savefig(savefile)

    plt.close()


def do_histplot(column, bins, xmax, zone, title, savefile, vlines=[]):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    column.plot.hist(bins=bins, range=(0, xmax), ax=ax)

    ax.grid(axis='y')

    ax.set_xlabel('Minutes')
    for vline in vlines:
        ax.axvline(vline).set_color('r')

    fig.suptitle('{} {}'.format(zone, title))

    plt.savefig(savefile)

    plt.close()


for plot in plots:

    basename = 'trips-{}'.format(plot['zone'])

    df = pd.read_csv(basename + '.csv', delimiter=',')

    # Create some new columns

    df.index = pd.to_datetime(df['Passenger_Arrival'])
    df.index = df.index.tz_convert('Europe/London')
    df = df.sort_index()

    df['Passenger_Duration_delta'] = pd.to_timedelta(df.Passenger_Duration, unit='S')
    df['Passenger_Duration_minutes'] = df.Passenger_Duration_delta.dt.total_seconds()/60

    df['Month'] = df.index.year * 100 + df.index.month

    # Drop records with Passenger_Duration below 0.5'th percentile or above 99.5'th
    df = df[(df.Passenger_Duration > df.Passenger_Duration.quantile(.01)) &
            (df.Passenger_Duration < df.Passenger_Duration.quantile(.99))]

    # Some filtered data frames
    df_weekdays = df[df.index.dayofweek < 5]
    df_weekdays_7_to_18 = df[(df.index.dayofweek < 5) & (df.index.hour >= 7) & (df.index.hour < 18)]
    df_saturday = df[df.index.dayofweek == 5]
    df_saturday_8_to_18 = df[(df.index.dayofweek == 5) & (df.index.hour >= 8) & (df.index.hour < 18)]
    df_sunday = df[df.index.dayofweek == 6]

    # ***** Passenger Duration

    do_histplot(
        df.Passenger_Duration_minutes, plot['max'], plot['max'], plot['zone'], 'all passenger trips',
        basename + '-passenger_trip-hist.pdf',
        vlines=(plot['duration'],
                plot['duration'] + plot['interval'],
                plot['duration'] + plot['sun-interval']))

    # =============== By hour of day, mon-fri

    do_boxplot(
        df_weekdays, df_weekdays.index.hour, 'Passenger_Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all passenger trips, by hour of day (Mon-Fri)',
        basename + '-passenger_trip-hod-mon_fri.pdf', hod=True,
        hlines=(plot['duration'], plot['duration'] + plot['interval']))

    # =============== By hour of day, sat

    do_boxplot(
        df_saturday, df_saturday.index.hour, 'Passenger_Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all passenger trips, by hour of day (Sat)',
        basename + '-passenger_trip-hod-sat.pdf',
        hlines=(plot['duration'], plot['duration'] + plot['interval']))

    # =============== By hour of day, sun

    do_boxplot(
        df_sunday, df_sunday.index.hour, 'Passenger_Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all passenger trips, by hour of day (Sun)',
        basename + '-passenger_trip-hod-sun.pdf',
        hlines=(plot['duration'], plot['duration'] + plot['sun-interval']))

    # =============== By month of year, mon-fri 07:00-18:00

    do_boxplot(
        df_weekdays_7_to_18, df_weekdays_7_to_18.Month, 'Passenger_Duration_minutes',
        '', plot['zone'], plot['max'], 'passenger trips, by month of year (Mon-Fri, 07:00-18:00)',
        basename + '-passenger_trip-moy-mon_fri.pdf', labels=months,
        hlines=(plot['duration'], plot['duration'] + plot['interval']))

    # =============== By month of year, Sat 08:00-18:00

    do_boxplot(
        df_saturday_8_to_18, df_saturday_8_to_18.Month, 'Passenger_Duration_minutes',
        '', plot['zone'], plot['max'], 'passenger trips, by month of year (Sat, 08:00-18:00)',
        basename + '-passenger_trip-moy-sat.pdf', labels=months,
        hlines=(plot['duration'], plot['duration'] + plot['interval']))

    # =============== By month of year, Sun

    do_boxplot(
        df_sunday, df_sunday.Month, 'Passenger_Duration_minutes',
        '', plot['zone'], plot['max'], 'passenger trips, by month of year (Sun)',
        basename + '-passenger_trip-moy-sun.pdf', labels=months,
        hlines=(plot['duration'], plot['duration'] + plot['sun-interval']))

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'Passenger_Duration_minutes',
        '', plot['zone'], plot['max'], 'passenger trips, by day of week',
        basename + '-passenger_trip-dow.pdf', labels=mon_fri,
        hlines=(plot['duration'],
                plot['duration'] + plot['interval']))
