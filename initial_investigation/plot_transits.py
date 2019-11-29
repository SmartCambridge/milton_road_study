#!/usr/bin/env python

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sns.set()
plt.rc('figure', figsize=(11.69, 8.27))

plots = [
    {'zone': 'milton_pandr_south',
     'max': 70,
     'duration': 16,
     'interval': 10,
     'sun-interval': 15
     },
    {'zone': 'milton_pandr_north',
     'max': 70,
     'duration': 20,
     'interval': 10,
     'sun-interval': 15
     },
]

mon_fri = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['Jan 2018', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
          'Jan 2019', 'Feb', 'Mar', 'Apr']


def fixup(zone_name):
    return zone_name.replace('_', ' ').replace('pandr', 'P&R').replace('milton', 'Milton')


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
        ax.axhline(hline[0]).set_color('r')
        ax.text(0.5, hline[0], hline[1], size=8, color='red', ha='left', va='bottom')

    ax.set_ylabel('Minutes')
    ax.set_ylim([0, ymax])
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))

    fig.suptitle('{} {}'.format(fixup(zone), title))

    plt.savefig(savefile)

    plt.close()


def do_histplot(column, bins, xmax, zone, title, savefile, vlines=[]):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    column.plot.hist(bins=bins, range=(0, xmax), ax=ax)

    ax.grid(axis='y')

    ax.set_ylim([0, 6000])

    ax.set_xlabel('Minutes')
    for vline in vlines:
        ax.axvline(vline[0]).set_color('r')
        ax.text(vline[0]+0.3, 5950, vline[1], size=8, color='red', rotation=90, ha='left', va='top')

    fig.suptitle('{} {}'.format(fixup(zone), title))

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

    # df['Worst_case'] = df.Interval_minutes + df.Duration_minutes

    df['Month'] = df.index.year * 100 + df.index.month

    # Drop records with Duration below 0.5'th percentile or above 99.5'th
    df = df[(df.Duration > df.Duration.quantile(.005)) &
            (df.Duration < df.Duration.quantile(.995))]

    # Some filtered data frames
    df_weekdays = df[df.index.dayofweek < 5]
    df_saturday = df[df.index.dayofweek == 5]
    df_sunday = df[df.index.dayofweek ==6]
    df_valid_intervals = df[(df.Interval_minutes < 60)]
    df_weekday_intervals = df[(df.Interval_minutes < 60) & (df.index.dayofweek < 5)]
    df_saturday_intervals = df[(df.Interval_minutes < 60) & (df.index.dayofweek == 5)]
    df_sunday_intervals = df[(df.Interval_minutes < 60) & (df.index.dayofweek == 6)]
    # Subset in on or after 07:00 (08:00 Saturdays), before 18:00 when timetabled interval in 10 min (15 min Saturdays)
    df_valid_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.hour >= 7) & (df.index.hour < 18)]
    df_weekday_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.hour >= 7) & (df.index.hour < 18) & (df.index.dayofweek < 5)]
    df_saturday_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.hour >= 8) & (df.index.hour < 18) & (df.index.dayofweek == 5)]
    df_sunday_intervals_subset = df[(df.Interval_minutes < 60) & (df.index.dayofweek == 6)]

    # ***** Trip Duration

    do_histplot(
        df.Duration_minutes, plot['max'], plot['max'], plot['zone'], 'all trip durations',
        basename + '-all_trip-hist.pdf', vlines=((plot['duration'], 'Timetable'),))

    # =============== By hour of day, mon-fri

    do_boxplot(
        df_weekdays, df_weekdays.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all trip durations, by hour of day (Mon-Fri)',
        basename + '-all_trip-hod-mon_fri.pdf', hod=True, hlines=((plot['duration'], 'Timetable'),))

    # =============== By hour of day, sat

    do_boxplot(
        df_saturday, df_saturday.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all trip durations, by hour of day (Sat)',
        basename + '-all_trip-hod-sat.pdf', hlines=((plot['duration'], 'Timetable'),))

    # =============== By hour of day, sun

    do_boxplot(
        df_sunday, df_sunday.index.hour, 'Duration_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all trip durations, by hour of day (Sun)',
        basename + '-all_trip-hod-sun.pdf', hlines=((plot['duration'], 'Timetable'),))

    # =============== By month of year, mon-fri

    do_boxplot(
        df_weekdays, df_weekdays.Month, 'Duration_minutes',
        '', plot['zone'], plot['max'], 'all trip durations, by month of year (Mon-Fri)',
        basename + '-all_trip-moy-mon_fri.pdf', labels=months, hlines=((plot['duration'], 'Timetable'),))

    # =============== By month of year, sat

    do_boxplot(
        df_saturday, df_saturday.Month, 'Duration_minutes',
        '', plot['zone'], plot['max'], 'all trip durations, by month of year (Sat)',
        basename + '-all_trip-moy-sat.pdf', labels=months, hlines=((plot['duration'], 'Timetable'),))

    # =============== By month of year, sun

    do_boxplot(
        df_sunday, df_sunday.Month, 'Duration_minutes',
        '', plot['zone'], plot['max'], 'all trip durations, by month of year (Sun)',
        basename + '-all_trip-moy-sun.pdf', labels=months, hlines=((plot['duration'], 'Timetable'),))

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'Duration_minutes',
        '', plot['zone'], plot['max'], 'all trip durations, by day of week',
        basename + '-all_trip-dow.pdf', labels=mon_fri, hlines=((plot['duration'], 'Timetable'),))

    # ***** Service interval

    do_histplot(
        df_valid_intervals.Interval_minutes, plot['max'], plot['max'], plot['zone'], 'all service intervals',
        basename + '-interval-hist.pdf', vlines=((plot['interval'], 'Timetable'),))

    # =============== By hour of day, mon-fri

    do_boxplot(
        df_weekday_intervals, df_weekday_intervals.index.hour, 'Interval_minutes',
        'Hour of day', plot['zone'], plot['max'], 'all service intervals, by hour of day (Mon-Fri)',
        basename + '-interval-hod-mon_fri.pdf', hlines=((plot['interval'], 'Timetable'),))

    # =============== By hour of day, saturday

    do_boxplot(
        df_saturday_intervals, df_saturday_intervals.index.hour, 'Interval_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all service intervals, by hour of day (Sat)',
        basename + '-interval-hod-sat.pdf', hlines=((plot['interval'], 'Timetable'),))

    # =============== By hour of day, sunday

    do_boxplot(
        df_sunday_intervals, df_sunday_intervals.index.hour, 'Interval_minutes',
        'Hour of Day', plot['zone'], plot['max'], 'all service intervals, by hour of day (Sun)',
        basename + '-interval-hod-sun.pdf', hlines=((plot['sun-interval'], 'Timetable'),))

    # =============== By month of year, mon-fri

    do_boxplot(
        df_weekday_intervals_subset, df_weekday_intervals_subset.Month, 'Interval_minutes',
        '', plot['zone'], plot['max'], 'service intervals, by month of year (Mon-Fri, 07:00-18:00)',
        basename + '-interval-moy-mon_fri.pdf', labels=months, hlines=((plot['interval'], 'Timetable'),))

    # =============== By month of year, saturdays

    do_boxplot(
        df_saturday_intervals_subset, df_saturday_intervals_subset.Month, 'Interval_minutes',
        '', plot['zone'], plot['max'], 'all service intervals, by month of year (Sat, 08:00-18:00)',
        basename + '-interval-moy-sat.pdf', labels=months, hlines=((plot['interval'], 'Timetable'),))

    # =============== By month of year, sundays

    do_boxplot(
        df_sunday_intervals_subset, df_sunday_intervals_subset.Month, 'Interval_minutes',
        '', plot['zone'], plot['max'], 'all service intervals, by month of year (Sun)',
        basename + '-interval-moy-sun.pdf', labels=months, hlines=((plot['sun-interval'], 'Timetable'),))

    # =============== By day of week

    do_boxplot(
        df_valid_intervals_subset, df_valid_intervals_subset.index.dayofweek, 'Interval_minutes',
        '', plot['zone'], plot['max'], 'all service intervals, by day of week (07:00-18:00)',
        basename + '-interval-dow.pdf', labels=mon_fri, hlines=((plot['interval'], 'Timetable'),))

    # # # == Worst case

    # do_histplot(
    #     df_valid_intervals.Worst_case, 100, 100, plot['zone'], 'worst trip duration',
    #     basename + '-worst-hist.pdf', vline=plot['interval'] + plot['duration'])

    # # =============== Sample, best/worst by month of year

    # do_boxplot(
    #     df_weekday_intervals_subset, df_weekday_intervals_subset.Month, 'Worst_case',
    #     '', plot['zone'], plot['max'], 'worst trip duration, by month (Mon-Fri, 07:00-18:00)',
    #     basename + '-worst-moy.pdf', labels=months, hline=plot['interval'] + plot['duration'])

    # # =============== Sample, best/worst by hour of day

    # do_boxplot(
    #     df_weekday_intervals, df_weekday_intervals.index.hour, 'Worst_case',
    #     'Hour of Day', plot['zone'], plot['max'], 'worst trip duration, by hour of day (Mon-Fri)',
    #     basename + '-worst-hod.pdf', hline=plot['interval'] + plot['duration'])

    # # =============== Sample,best/worst by day of week

    # do_boxplot(
    #     df_valid_intervals_subset, df_valid_intervals_subset.index.dayofweek, 'Worst_case',
    #     '', plot['zone'], plot['max'], 'worst trip duration, by day of week (Mon-Fri, 07:00-18:00)',
    #     basename + '-worst-dow.pdf', labels=mon_fri, hline=plot['interval'] + plot['duration'])

    # # Best/Worst compared

    # best_sum = df_weekday_intervals_subset.Duration_minutes.groupby(df_weekday_intervals_subset.index.hour).quantile(0.75)
    # worst_sum = df_weekday_intervals_subset.Worst_case.groupby(df_weekday_intervals_subset.index.hour).quantile(0.75)

    # df_plot = pd.concat([best_sum, worst_sum], axis = 1)

    # fig, ax = plt.subplots(nrows=1, ncols=1)

    # ax.bar(df_plot.index, df_plot.Worst_case, bottom=df_plot.Duration_minutes, fill=False, edgecolor=['b'])
    # ax.grid(axis='x')
    # ax.set_ylim([0, plot['max']])
    # ax.set_xlabel('Hour of day')
    # ax.set_ylabel('Minutes')
    # ax.axhline(plot['duration']).set_color('g')
    # ax.axhline(plot['duration'] + plot['interval']).set_color('r')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    # fig.suptitle('{} {}'.format(plot['zone'], 'Best and worst journeys, 75\'th percentile (Mon-Fri, 07:00 - 18:00)'))
    # plt.savefig(basename + '-best_worst.pdf')
    # plt.close()
