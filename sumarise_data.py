#!/usr/bin/env python

import numpy as np
import pandas as pd

plots = [
    {'year': 2019,
     'zone': 'a428_east'
     },
    {'year': 2019,
     'zone': 'a428_west'
     },
    {'year': 2019,
     'zone': 'a1m_north'
     },
    {'year': 2019,
     'zone': 'a1m_south'
     },
]


def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_


for ctr, plot in enumerate(plots):

    basename = 'transits-{}-{}'.format(plot['zone'], plot['year'])

    df = pd.read_csv(basename + '.csv', delimiter=',')
    df['Date'] = pd.to_datetime(df['Date'])
    df.index = df['Date']
    del df['Date']

    df['D'] = df.index.date

    sum = df.groupby(['D']).Duration.agg(
        [('Min', 'min'),
         ('Q1', percentile(25)),
         ('Median', 'median'),
         ('Q3', percentile(75)),
         ('Max', 'max')
         ]
    )

    sum.to_csv(basename + '_sumary.csv',)
