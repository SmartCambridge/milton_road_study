#!/usr/bin/env python3

"""
From a set of zone transits representing trips between stops, work out
the effective trip time for a passenger arriving at the the origin every
minute from the departure time of the first bus to the departure time of
the last one
"""

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
    'Trip_Departure',
    'Trip_Arrival',
    'Trip_Duration',
    'Passenger_Journey_Duration',
]

for zone in zones:

    logger.debug('Processing %s', zone)

    in_filename = 'transits-{}.csv'.format(zone)
    logger.debug('Reading %s', in_filename)
    with open(in_filename, 'r', newline='') as in_file:
        in_headers = next(in_file)

        out_filename = 'trips-{}.csv'.format(zone)
        logger.debug('Writing %s', out_filename)
        with open(out_filename, 'w', newline='') as out_file:

            for row in in_file:

                raw_arrival, raw_duration, raw_distance = row

                arrival = isodate.parse_datetime(raw_arrival)
                duration = 
                departure = arrival - duration







# Build a table of trip times
trip_table = []
for segment in segments['segments']:
    if not segment['on_route']:
        continue
    departure = isodate.parse_datetime(segment['positions'][0]['RecordedAtTime'])
    arrival = isodate.parse_datetime(segment['positions'][-1]['RecordedAtTime'])
    trip_table.append([departure, arrival, segment['VehicleRef']])

# Find the top of the hour before the first bus
start = trip_table[0][0].replace(minute=0, second=0)
# And the top of the hour after the last one
end = trip_table[-1][0].replace(minute=0, second=0) + datetime.timedelta(hours=1)
step = datetime.timedelta(minutes=1)

logger.debug("Start %s, end %s, step %s", start, end, step)

# Step through the day from 'start' to 'end' in steps of 'step'
# Find the next bus to depart after 'start'
while start < end:
    # Find first departure after 'start'
    for row in trip_table:
        logger.debug("row[1]: %s, start: %s", row[1], start)
        if row[0] > start:
            wait = int((row[0] - start).total_seconds())
            traveling = int((row[1] - row[0]).total_seconds())
            duration = wait + traveling
            values.append([
                start,
                wait,
                row[2],
                row[0],
                row[1],
                traveling,
                duration,
            ])
            break
    else:
        logger.debug("No bus for a departure at %s", start)

    start = start + step

return header, values


def emit_csv(basename, header, values):

    csv_filename = '{}-expanded.csv'.format(basename)
    logger.info('Outputing CSV to %s', csv_filename)

    with open(csv_filename, 'w', newline='') as csvfile:

        # Create CSV, add headers
        output = csv.writer(csvfile, dialect='excel', quoting=csv.QUOTE_ALL)
        output.writerow(header)
        output.writerows(values)


def main():

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    logger.info('Start')

    basename = sys.argv[1]

    segments = load_segments(basename)

    header, values = sumarise(segments)

    emit_csv(basename, header, values)

    logger.info('Stop')


if __name__ == "__main__":
    main()
