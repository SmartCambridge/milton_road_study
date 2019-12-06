#!/usr/bin/env python

import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


sns.set()
plt.rc('figure', figsize=(11.69, 8.27))


mon_fri = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

months = ['Nov 2018', 'Dec',
          'Jan 2019', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']


def format_dow(raw):
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


def do_boxplot(df, by, column, xlabel, ylabel, ymax, title,
               savefile, suptitle, source_tag, labels=None, hod=False):

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
    if labels is not None:
        ax.set_xticklabels(labels)
    elif hod:
        ax.set_xticklabels([format_dow(int(x.get_text())) for x in ax.get_xticklabels()])

    ax.set_ylabel(ylabel)
    ax.set_ylim([0, ymax])
    ax.set_title(title)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(25))

    fig.suptitle(suptitle)

    plt.savefig(source_tag + '-' + savefile)

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
    ax.set_title(title)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}%'))

    fig.suptitle(suptitle)

    plt.savefig(source_tag + '-' + savefile)

    plt.close()


def do_graph_set(df, suptitle, source_tag, count_max):

    # =============== Distribution

    do_histplot(df.minutes, 48, 24, 30, 'Journey time distribution',
                'hist.pdf', suptitle, source_tag)

    # =============== By hour of day

    MINUTES_YMAX = 24

    do_boxplot(
        df, 100*df.index.hour+df.index.minute, 'minutes',
        'Time of Day', 'Minutes', MINUTES_YMAX, 'Journey time by time of day',
        'minutes-tod.pdf', suptitle, source_tag, hod=True)

    do_boxplot(
        df, 100*df.index.hour+df.index.minute, 'count',
        'Time of Day', 'Journeys per sample', count_max, 'Sample sizes by time of day',
        'count-tod.pdf', suptitle, source_tag, hod=True)

    # =============== By month of year, mon-fri 07:00-18:00

    do_boxplot(
        df, df.Month, 'minutes',
        '', 'Minutes', MINUTES_YMAX, 'Journey time by month',
        'minutes-month.pdf', suptitle, source_tag, labels=months)

    do_boxplot(
        df, df.Month, 'count',
        '', 'Journeys per sample', count_max, 'Sample sizes by month',
        'count-month.pdf', suptitle, source_tag, labels=months)

    # =============== By day of week

    do_boxplot(
        df, df.index.dayofweek, 'minutes',
        '', 'Minutes', MINUTES_YMAX, 'Journey time by day of week',
        'minutes-dow.pdf', suptitle, source_tag, labels=mon_fri)

    do_boxplot(
        df, df.index.dayofweek, 'count',
        '', 'Journeys per sample', count_max, 'Sample sizes by day of week',
        'count-dow.pdf', suptitle, source_tag, labels=mon_fri)

    # =============== Grand summary

    do_boxplot(
        df, None, 'minutes',
        '', 'Minutes', MINUTES_YMAX, 'All journey times',
        'minutes-overall.pdf', suptitle, source_tag, labels=[])

    do_boxplot(
        df, None, 'count',
        '', 'Journeys per sample', count_max, 'Journeys per sample',
        'count-overall.pdf', suptitle, source_tag, labels=[])


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

    # Subset to >+ 07:30 and < 09:30, Mon-Fri with more than 10 observations
    # in each part
    df = df[
            (
               ((df.index.hour == 7) & (df.index.minute >= 30)) |
               (df.index.hour == 8) |
               ((df.index.hour == 9) & (df.index.minute < 30))
            )
            &
            (
               df.index.dayofweek < 5
            )
            &
            (
               (df['count_north'] >= 10) & (df['count_south'] >= 10)
            )
           ]

    return df


def get_bus_data():

    DATAFILE = 'bus/transits-milton_road_2_in.csv'

    # "Date","Duration","Distance"

    df_raw = pd.read_csv(DATAFILE)

    df_raw.index = pd.to_datetime(df_raw['Date'])
    df_raw = df_raw.sort_index()

    df = pd.DataFrame()
    df['Duration'] = df_raw.Duration.resample('15min').median()
    df['Distance'] = df_raw.Distance.resample('15min').median()
    df['count'] = df_raw.Duration.resample('15min').count()

    df['minutes'] = df.Duration/60
    df['Month'] = df.index.year * 100 + df.index.month

    # Subset to >+ 07:30 and < 09:30, Mon-Fri with at least 1 observations
    df = df[
            (
              ((df.index.hour == 7) & (df.index.minute >= 30)) |
              (df.index.hour == 8) |
              ((df.index.hour == 9) & (df.index.minute < 30))
            )
            &
            (
              df.index.dayofweek < 5
            )
            &
            (
              df['count'] > 0
            )
           ]

    return df

# === Drakewell 'bluetruth'


df = get_drakewell_data()
print('Drakewell data:')
print(df.describe())

suptitle = ('All traffic (\'Bluetruth\') Journey Times\n'
            'Milton Road (A14 to Arbury Rd/Union Ln), Nov 2018-Oct 2019, 07:30-09:30'
            )

do_graph_set(df, suptitle, 'drakewell', 100)

# Try to understand drop in sample size July 2019
do_boxplot(
    df, df.Month, 'count_north',
    '', 'Journeys per sample', 100, 'Sample sizes by month - 9800X7003HZY',
    'count-month-north.pdf', suptitle, 'drakewell', labels=months)

do_boxplot(
    df, df.Month, 'count_south',
    '', 'Journeys per sample', 100, 'Sample sizes by month - 9800YU0FYRKZ',
    'count-month-south.pdf', suptitle, 'drakewell', labels=months)

# === SmartCambridge Zone transot data

df = get_bus_data()
print('Bus data:')
print(df.describe())

suptitle = ('Bus Journey Times\n'
            'Milton Road (Busway to Elizabeth Way), Nov 2018-Oct 2019, 07:30-09:30'
            )

do_graph_set(df, suptitle, 'bus', 10)
