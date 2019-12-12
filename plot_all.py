#!/usr/bin/env python

import datetime
import json
import os

import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

PDF_DIR = 'pdf'


sns.set()
plt.rc('figure', figsize=(11.69, 8.27))


mon_fri = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['Nov 2018', 'Dec',
          'Jan 2019', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']

months_vivacity = ['May 2019', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']


def time_filter(df):
    '''
    Filter data frame to just contain records 07:30..09:30
    '''

    return df[
                (
                   ((df.index.hour == 7) & (df.index.minute >= 30)) |
                   (df.index.hour == 8) |
                   ((df.index.hour == 9) & (df.index.minute < 30))
                )
             ]


def format_hod(raw):
    '''
    Given a number like 930 representing  the time '09:30', return a
    formatted label for the time range from this time to one 15 min in
    the future.
    '''

    h_start = raw // 100
    m_start = raw % 100
    h_end = h_start
    m_end = m_start + 15
    if m_end > 59:
        h_end += 1
        m_end = m_end - 60
    return('{:02d}:{:02d}-{:02d}:{:02d}'.format(h_start, m_start, h_end, m_end))


def format_hod1(raw):
    '''
    Given a number like 930 representing  the time '09:30', return a
    formatted label for the hour if minutes are 0 and '' otherwise
    '''

    h_start = raw // 100
    m_start = raw % 100
    return '{:02d}'.format(h_start) if m_start == 0 else ''


def do_boxplot(df, by, column, xlabel, ylabel, ymax, title,
               savefile, suptitle, source_tag, labels=None, hod=False, hod1=False):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    flierprops = dict(markersize=5, marker='.')

    df.boxplot(
        by=by,
        column=column,
        grid=False,
        # whis='range',
        whis=(5, 95),
        flierprops=flierprops,
        ax=ax)

    ax.set_title('')
    ax.grid(axis='y')

    ax.set_xlabel(xlabel)
    if labels is not None:
        ax.set_xticklabels(labels)
    elif hod:
        ax.set_xticklabels([format_hod(int(x.get_text())) for x in ax.get_xticklabels()])
    elif hod1:
        ax.set_xticklabels([format_hod1(int(x.get_text())) for x in ax.get_xticklabels()])

    ax.set_ylabel(ylabel)
    ax.set_ylim([0, ymax])
    ax.set_title('(5th, 25th, 50th, 75th and 95th percentiles)')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=25, steps=[1, 2, 5, 10], integer=True))

    fig.suptitle(suptitle + ' ' + title)

    plt.savefig(os.path.join(PDF_DIR, source_tag + '-' + savefile))

    plt.close()


def do_histplot(column, bins, xmax, ymax, title, savefile, suptitle, source_tag):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    # Add weights to make the bars sum to 100
    column.plot.hist(bins=bins, range=(0, xmax), ax=ax,
                     weights=100 * np.ones(len(column)) / len(column))

    ax.grid(axis='y')

    ax.set_ylim([0, ymax])
    ax.set_xlim([0, xmax])

    print(column.max())

    ax.axvline(x=column.max(), linestyle='--')
    ax.annotate('Max', xy=(column.max(), 0.9), xycoords=('data', 'axes fraction'),
                xytext=(-30, 0), textcoords='offset points',
                ha='right', arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle="->"))

    ax.set_xlabel('Minutes')
    ax.set_ylabel('Proportion of journeys')
    ax.set_title('')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}%'))

    fig.suptitle(suptitle + ' ' + title)

    plt.savefig(os.path.join(PDF_DIR, source_tag + '-' + savefile))

    plt.close()


def do_journey_time_graph_set(df, suptitle, source_tag, count_max):

    MINUTES_YMAX = 40

    # =============== Distribution

    do_histplot(df.minutes, 2*MINUTES_YMAX, MINUTES_YMAX, 20, 'journey duration distribution',
                'hist.pdf', suptitle, source_tag)

    # =============== By hour of day

    do_boxplot(
        df, 100*df.index.hour+df.index.minute, 'minutes',
        'Time of Day', 'Minutes', MINUTES_YMAX, 'journey duration by time of day',
        'minutes-tod.pdf', suptitle, source_tag, hod=True)

    do_boxplot(
        df, 100*df.index.hour+df.index.minute, 'count',
        'Time of Day', 'Journeys per sample', count_max, 'sample sizes by time of day',
        'count-tod.pdf', suptitle, source_tag, hod=True)

    # =============== By month of year, mon-fri 07:00-18:00

    do_boxplot(
        df, df.Month, 'minutes',
        '', 'Minutes', MINUTES_YMAX, 'journey duration by month',
        'minutes-month.pdf', suptitle, source_tag, labels=months)

    do_boxplot(
        df, df.Month, 'count',
        '', 'Journeys per sample', count_max, 'sample sizes by month',
        'count-month.pdf', suptitle, source_tag, labels=months)

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'minutes',
        '', 'Minutes', MINUTES_YMAX, 'journey duration by day of week',
        'minutes-dow.pdf', suptitle, source_tag, labels=mon_fri)

    do_boxplot(
        df, df.index.dayofweek, 'count',
        '', 'Journeys per sample', count_max, 'sample sizes by day of week',
        'count-dow.pdf', suptitle, source_tag, labels=mon_fri)

    # =============== Grand summary

    do_boxplot(
        df, None, 'minutes',
        '', 'Minutes', MINUTES_YMAX, 'journey durations',
        'minutes-overall.pdf', suptitle, source_tag, labels=[])

    do_boxplot(
        df, None, 'count',
        '', 'Journeys per sample', count_max, 'sample sizes',
        'count-overall.pdf', suptitle, source_tag, labels=[])


def do_vehicle_count_graph_set(df, suptitle, source_tag, vcount_max, bcount_max):

    # === by time of day

    do_boxplot(
        df, 100*df.index.hour+df.index.minute, 'motor_total',
        'Time of Day', 'Journeys per sample', vcount_max, 'Number of motor journeys by time of day',
        'all-count-tod.pdf', suptitle, source_tag, hod=True)

    do_boxplot(
        df, 100*df.index.hour+df.index.minute, 'bus',
        'Time of Day', 'Journeys per sample', bcount_max, 'Number of bus journeys by time of day',
        'bus-count-tod.pdf', suptitle, source_tag, hod=True)

    # =============== By month of year, mon-fri 07:00-18:00

    do_boxplot(
        df, df.Month, 'motor_total',
        '', 'Journeys per sample', vcount_max, 'Number of motor journeys by month',
        'all-count-month.pdf', suptitle, source_tag, labels=months_vivacity)

    do_boxplot(
        df, df.Month, 'bus',
        '', 'Journeys per sample', bcount_max, 'Number of bus journeys by month',
        'bus-count-month.pdf', suptitle, source_tag, labels=months_vivacity)

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'motor_total',
        '', 'Journeys per sample', vcount_max, 'Number of bus journeys by day of week',
        'all-count-dow.pdf', suptitle, source_tag, labels=mon_fri)

    do_boxplot(
        df, df.index.dayofweek, 'bus',
        '', 'Journeys per sample', bcount_max, 'Number of bus journeys by day of week',
        'bus-count-dow.pdf', suptitle, source_tag, labels=mon_fri)

    # =============== Grand summary

    do_boxplot(
        df, None, 'motor_total',
        '', 'Journeys per sample', vcount_max, 'Number of motor journeys',
        'all-count-overall.pdf', suptitle, source_tag, labels=[])

    do_boxplot(
        df, None, 'bus',
        '', 'Journeys per sample', bcount_max, 'Number of bus journeys per sample',
        'bus-count-overall.pdf', suptitle, source_tag, labels=[])


def get_drakewell_data():

    # Node,Cosit,Time,Period (s),Journey Time (s),Match Count

    DATAFILES_NORTH = [
        'drakewell/data/9800X7003HZY-2018-11.csv',
        'drakewell/data/9800X7003HZY-2018-12.csv',
        'drakewell/data/9800X7003HZY-2019-01.csv',
        'drakewell/data/9800X7003HZY-2019-02.csv',
        'drakewell/data/9800X7003HZY-2019-03.csv',
        'drakewell/data/9800X7003HZY-2019-04.csv',
        'drakewell/data/9800X7003HZY-2019-05.csv',
        'drakewell/data/9800X7003HZY-2019-06.csv',
        'drakewell/data/9800X7003HZY-2019-07.csv',
        'drakewell/data/9800X7003HZY-2019-08.csv',
        'drakewell/data/9800X7003HZY-2019-09.csv',
        'drakewell/data/9800X7003HZY-2019-10.csv',
    ]

    DATAFILES_SOUTH = [
        'drakewell/data/9800YU0FYRKZ-2018-11.csv',
        'drakewell/data/9800YU0FYRKZ-2018-12.csv',
        'drakewell/data/9800YU0FYRKZ-2019-01.csv',
        'drakewell/data/9800YU0FYRKZ-2019-02.csv',
        'drakewell/data/9800YU0FYRKZ-2019-03.csv',
        'drakewell/data/9800YU0FYRKZ-2019-04.csv',
        'drakewell/data/9800YU0FYRKZ-2019-05.csv',
        'drakewell/data/9800YU0FYRKZ-2019-06.csv',
        'drakewell/data/9800YU0FYRKZ-2019-07.csv',
        'drakewell/data/9800YU0FYRKZ-2019-08.csv',
        'drakewell/data/9800YU0FYRKZ-2019-09.csv',
        'drakewell/data/9800YU0FYRKZ-2019-10.csv',
    ]

    # Data from 9800X7003HZY
    df_north = pd.concat(map(pd.read_csv, DATAFILES_NORTH))
    df_north.columns = ['node', 'cosit', 'timestamp', 'period', 'seconds', 'count']

    # Data from 9800YU0FYRKZ
    df_south = pd.concat(map(pd.read_csv, DATAFILES_SOUTH))
    df_south.columns = ['node', 'cosit', 'timestamp', 'period', 'seconds', 'count']

    # Merge the links
    df = pd.merge(df_north, df_south, on='timestamp', how='inner', suffixes=('_north', '_south'))

    df['seconds'] = df.seconds_north + df.seconds_south
    df['minutes'] = df.seconds/60
    df['count'] = df.count_north + df.count_south

    # Build an index on datetime
    df.index = pd.to_datetime(df['timestamp'])
    df.index = df.index.tz_localize('Europe/London', ambiguous='NaT')
    df = df.sort_index()
    df.drop('timestamp', axis=1, inplace=True)

    # Hacked-up month representation
    df['Month'] = df.index.year * 100 + df.index.month

    # Subset to Mon-Fri with more than 10 observations in each half
    df = df[
            (
               df.index.dayofweek < 5
            )
            &
            (
               (df.count_north >= 10) & (df.count_south >= 10)
            )
           ]

    return df


def get_bus_data():

    DATAFILE = 'bus/transits-milton_road_alternate_in.csv'

    # "Date","Duration","Distance"

    df_raw = pd.read_csv(DATAFILE)

    df_raw.index = pd.to_datetime(df_raw['Date'])
    df_raw = df_raw.sort_index()

    df = pd.DataFrame()
    df['Duration'] = df_raw.Duration.resample('15min').mean()
    df['Distance'] = df_raw.Distance.resample('15min').mean()
    df['count'] = df_raw.Duration.resample('15min').count()

    df['minutes'] = df.Duration/60
    df['Month'] = df.index.year * 100 + df.index.month

    # Subset to Mon-Fri with at least 1 observations of less that 2 hours
    df = df[
            (
              df.index.dayofweek < 5
            )
            &
            (
              df['count'] > 0
            )
            &
            (
              df.Duration < 7200  # 2 hours
            )
           ]

    return df


def get_vivacity_data():

    '''
    Retrieve data for `countline` in `direction` between the days
    from `start` to `end`. Input format below. Output is a 2D array
    with one row per sample.

    {
        "ts": 1562284800.0,
        "timestamp": "2019-07-05T00:00:00+00:00",
        "from": "2019-07-05T00:00:00.000Z",
        "to": "2019-07-05T00:05:00.000Z",
        "countline": "13069",
        "direction": "in",
        "counts": {
            "pedestrian": 1,
            "cyclist": 0,
            "motorbike": 1,
            "car": 1,
            "taxi": 0,
            "van": 1,
            "minibus": 0,
            "bus": 0,
            "rigid": 0,
            "truck": 0,
            "emergency car": 0,
            "emergency van": 0,
            "fire engine": 0
        }
    }
    ...
    '''

    VCLASSES = ("pedestrian", "cyclist", "motorbike", "car",
                "taxi", "van", "minibus", "bus", "rigid",
                "truck", "emergency car", "emergency van",
                "fire engine")

    ONE_DAY = datetime.timedelta(days=1)

    start = datetime.date(2018, 11, 1)
    end = datetime.date(2019, 10, 31)
    countline = '13079'

    day = start
    data = []
    while day <= end:

        try:
            filename = os.path.join(
                'vivacity', 'vivacity_data/',
                day.strftime('%Y'),
                day.strftime('%m'),
                day.strftime('%d'),
                countline,
                'in.txt')
            with open(filename) as file:
                for line in file:
                    data_block = json.loads(line)
                    row = ([data_block['timestamp']] +
                           [data_block['counts'][key] for key in VCLASSES])
                    data.append(row)
        except FileNotFoundError:
            pass
        day += ONE_DAY

    df_raw = pd.DataFrame(data)
    df_raw.columns = ('timestamp',) + VCLASSES

    df_raw.index = pd.to_datetime(df_raw['timestamp'])
    df_raw = df_raw.sort_index()
    df_raw.drop('timestamp', axis=1, inplace=True)

    df = pd.DataFrame()
    for key in VCLASSES:
        df[key] = df_raw[key].resample('15min').sum()
    df['count'] = df_raw.pedestrian.resample('15min').count()

    df['motor_total'] = 0
    for key in [v for v in VCLASSES if v not in ('pedestrian', 'cyclist')]:
        df['motor_total'] = df['motor_total'] + df[key]
    df.motor_total.replace(0, np.nan, inplace=True)

    df.bus.replace(0, np.nan, inplace=True)

    df['Month'] = df.index.year * 100 + df.index.month

    # Subset to Mon-Fri with at least 1 observations
    df = df[
            (
              df.index.dayofweek < 5
            )
            &
            (
              df['count'] > 0
            )
           ]

    return df


os.makedirs(PDF_DIR, exist_ok=True)

# === Drakewell 'bluetruth'

df_drakewell = get_drakewell_data()
df_drakewell = time_filter(df_drakewell)
print('Drakewell data:')
print(df_drakewell.describe())

suptitle = ('\'All traffic\'')

do_journey_time_graph_set(df_drakewell, suptitle, 'drakewell', 100)


# === SmartCambridge Zone transot data

df_bus = get_bus_data()
df_bus = time_filter(df_bus)
print('Bus data:')
print(df_bus.describe())

suptitle = ('Bus')

do_journey_time_graph_set(df_bus, suptitle, 'bus', 10)

# === Vivacity traffic counts

df = get_vivacity_data()
df = time_filter(df)
print('Vivacity data:')
print(df.describe())

suptitle = ('')

do_vehicle_count_graph_set(df, suptitle, 'vivacity', 200, 20)

# === combined Drakewell/bus

df = pd.merge(df_drakewell, df_bus, how='outer', left_index=True, right_index=True, suffixes=('_drakewell', '_bus'))
print('Combined data:')
print(df.describe())

do_boxplot(
    df, None, ['minutes_bus', 'minutes_drakewell'],
    '', 'Minutes', 40, 'journey durations',
    'minutes-overall.pdf', 'All', 'both', labels=['Bus', 'All trafic'])
