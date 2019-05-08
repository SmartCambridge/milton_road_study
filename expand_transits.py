#!/usr/bin/env python3

"""
From a set of zone transits representing trips between stops, work out
the effective trip time for a passenger arriving at the the origin every
minute from the departure time of the first bus to the departure time of
the last one
"""

import collections
import datetime
import logging
import sys
import csv

import isodate

zones = ['milton_pandr_south', 'milton_pandr_north']

logger = logging.getLogger('__name__')

header = [
    'Passenger_Arrival',
    'Passenger_Wait',
    'Bus_Departure',
    'Bus_Arrival',
    'Bus_Duration',
    'Passenger_Duration',
]


def process_zones():

    for zone in zones:

        logger.debug('Processing %s', zone)

        # Read in...

        in_filename = 'transits-{}.csv'.format(zone)
        logger.info('Reading %s', in_filename)

        with open(in_filename, 'r', newline='') as in_file:
            input = csv.reader(in_file, dialect='excel', quoting=csv.QUOTE_ALL)
            next(input)   # Skip headers
            trip_table = collections.OrderedDict()
            for row in input:

                trip = {}
                raw_arrive, raw_duration, raw_distance = row
                trip['arrive'] = isodate.parse_datetime(raw_arrive)
                trip['duration'] = datetime.timedelta(seconds=float(raw_duration))
                trip['depart'] = trip['arrive'] - trip['duration']
                day = trip['depart'].date()
                trip['distance'] = float(raw_distance)

                if day not in trip_table:
                    trip_table[day] = []
                trip_table[day].append(trip)

        # ... write out

        step = datetime.timedelta(minutes=1)

        out_filename = 'trips-{}.csv'.format(zone)
        logger.info('writing %s', out_filename)
        with open(out_filename, 'w', newline='') as out_file:
            output = csv.writer(out_file, dialect='excel', quoting=csv.QUOTE_ALL)
            output.writerow(header)

            for day in trip_table:
                logger.info('Processing %s %s', zone, day)
                todays_trips = trip_table[day]

                # Find the minute before the first bus of the day
                start = todays_trips[0]['depart'].replace(second=0)
                # And the last departure of the day
                end = todays_trips[-1]['depart']

                logger.debug("Start %s, end %s, step %s", start, end, step)

                # Step through the day from 'start' to 'end' in steps of 'step'
                # Find the next bus to depart after 'start'
                while start < end:
                    # Find first departure after 'start'
                    for row in todays_trips:
                        logger.debug("row depart: %s, start: %s", row['depart'], start)
                        if row['depart'] > start:
                            wait = int((row['depart'] - start).total_seconds())
                            traveling = int((row['duration']).total_seconds())
                            trip_duration = wait + traveling
                            output.writerow([
                                start,
                                wait,
                                row['depart'],
                                row['arrive'],
                                traveling,
                                trip_duration,
                            ])
                            break
                    else:
                        logger.error("No bus for a departure at %s", start)

                    start = start + step


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    logger.info('Start')

    process_zones()

    logger.info('Stop')


if __name__ == "__main__":
    main()
