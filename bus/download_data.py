#!/usr/bin/env python3

import csv
import datetime
import logging
import os

import coreapi
from dateutil.relativedelta import relativedelta

logger = logging.getLogger('__name__')

API_SCHEMA = os.getenv('API_SCHEMA', 'https://smartcambridge.org/api/docs/')

API_TOKEN = os.getenv('API_TOKEN', None)
assert API_TOKEN, 'API_TOKEN environment variable not set'

zones = ['milton_road_2_in']

first = datetime.date(2018, 11, 1)
last = datetime.date(2019, 10, 1)

def get_data():

    auth = coreapi.auth.TokenAuthentication(
        scheme='Token',
        token=API_TOKEN
    )
    client = coreapi.Client(auth=auth)

    schema = client.get(API_SCHEMA)

    action = ['zone', 'history', 'read']

    for zone in zones:

        csv_filename = 'transits-{}.csv'.format(zone)
        logger.info('Outputting CSV to %s', csv_filename)

        with open(csv_filename, 'w', newline='') as csvfile:

            output = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
            output.writerow(['Date', 'Duration', 'Distance'])

            date = first

            while date <= last:

                ctr = 0

                start = date.strftime('%Y-%m-%d')
                end = (date + relativedelta(day=31)).strftime('%Y-%m-%d')

                params = {
                    'zone_id': zone,
                    'start_date': start,
                    'end_date': end
                }
                logger.debug("Getting transits, zone %s, start %s, end %s", zone, start, end)
                api_results = client.action(schema, action, params=params)
                for result in api_results['request_data']:
                    ctr += 1
                    output.writerow([
                        result['date'],
                        result['duration'],
                        result['distance']
                    ])

                date = date + relativedelta(months=1)

        logger.info('Wrote %s records', ctr)


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    get_data()


if __name__ == "__main__":
    main()
