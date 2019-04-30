#!/usr/bin/env python3

import csv
import datetime
import logging
import os

import coreapi


logger = logging.getLogger('__name__')

API_SCHEMA = os.getenv('API_SCHEMA', 'https://tfc-app1.cl.cam.ac.uk/api/docs/')

API_TOKEN = os.getenv('API_TOKEN', None)
assert API_TOKEN, 'API_TOKEN environment variable not set'

stops = [
   {'atcocode': '0500SMILT010',
    'direction': 'south',
    },
   {'atcocode': '0500CCITY486',
    'direction': 'north',
    }
]

day = '2019-04-30'


def get_data():

    auth = coreapi.auth.TokenAuthentication(
        scheme='Token',
        token=API_TOKEN
    )
    client = coreapi.Client(auth=auth)

    schema = client.get(API_SCHEMA)

    action = ['transport', 'journeys_by_time_and_stop', 'list']

    for stop in stops:

        stop_id = stop['atcocode']
        direction = stop['direction']
        datetime_from = day + 'T00:00:00'

        csv_filename = 'timetable-{}.csv'.format(direction)
        logger.info('Outputting CSV to %s', csv_filename)

        with open(csv_filename, 'w', newline='') as csvfile:

            output = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
            output.writerow(['Depart', 'Arrive', 'Duration', 'Wait'])

            params = {
                'stop_id': stop_id,
                'datetime_from': datetime_from,
                'nresults': '10000',
                'expand_journey': True
            }

            logger.debug("Getting journeys, stop_id %s, datetime_from %s", stop_id, datetime_from)
            api_results = client.action(schema, action, params=params)

            previous_depart = None

            for result in api_results['results']:
                timetable = result['journey']['timetable']

                # SKip if not the Milton Road Park & Ride service or
                # not leaving from our expected stop
                if ((result['line']['line_name'] != 'Milton Road Park & Ride') or
                   (timetable[0]['stop']['atco_code'] != stop_id)):
                    continue

                # print(result['time'],
                #      result['journey']['timetable'][0]['time'],
                #      result['journey']['timetable'][0]['stop']['atco_code'])

                timetable = result['journey']['timetable']

                depart = datetime.datetime.strptime(
                    day + 'T' + timetable[0]['time'],
                    '%Y-%m-%dT%H:%M:%S')
                arrive = datetime.datetime.strptime(
                    day + 'T' + timetable[-1]['time'],
                    '%Y-%m-%dT%H:%M:%S')
                duration = arrive - depart
                if previous_depart:
                    wait = depart - previous_depart
                    output.writerow([
                        depart,
                        arrive,
                        duration.total_seconds(),
                        wait.total_seconds()
                    ])
                else:
                    output.writerow([
                        depart,
                        arrive,
                        duration.total_seconds(),
                        None
                    ])

                previous_depart = depart


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    get_data()


if __name__ == "__main__":
    main()
