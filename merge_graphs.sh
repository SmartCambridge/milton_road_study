#!/bin/bash

# Collect graphs into one big file in a sane order

"/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py" \
-o graphs.pdf                                        \
transits-milton_pandr_south-all_trip-hist.pdf        \
transits-milton_pandr_north-all_trip-hist.pdf        \
transits-milton_pandr_south-all_trip-moy-mon_fri.pdf \
transits-milton_pandr_north-all_trip-moy-mon_fri.pdf \
transits-milton_pandr_south-all_trip-moy-sat.pdf \
transits-milton_pandr_north-all_trip-moy-sat.pdf \
transits-milton_pandr_south-all_trip-moy-sun.pdf \
transits-milton_pandr_north-all_trip-moy-sun.pdf \
transits-milton_pandr_south-all_trip-dow.pdf         \
transits-milton_pandr_north-all_trip-dow.pdf         \
transits-milton_pandr_south-all_trip-hod-mon_fri.pdf \
transits-milton_pandr_north-all_trip-hod-mon_fri.pdf \
transits-milton_pandr_south-all_trip-hod-sat.pdf \
transits-milton_pandr_north-all_trip-hod-sat.pdf \
transits-milton_pandr_south-all_trip-hod-sun.pdf \
transits-milton_pandr_north-all_trip-hod-sun.pdf \
transits-milton_pandr_south-interval-hist.pdf        \
transits-milton_pandr_north-interval-hist.pdf        \
transits-milton_pandr_south-interval-moy-mon_fri.pdf \
transits-milton_pandr_north-interval-moy-mon_fri.pdf \
transits-milton_pandr_south-interval-moy-sat.pdf \
transits-milton_pandr_north-interval-moy-sat.pdf \
transits-milton_pandr_south-interval-moy-sun.pdf \
transits-milton_pandr_north-interval-moy-sun.pdf \
transits-milton_pandr_south-interval-dow.pdf         \
transits-milton_pandr_north-interval-dow.pdf         \
transits-milton_pandr_south-interval-hod-mon_fri.pdf \
transits-milton_pandr_north-interval-hod-mon_fri.pdf \
transits-milton_pandr_south-interval-hod-sat.pdf \
transits-milton_pandr_north-interval-hod-sat.pdf \
transits-milton_pandr_south-interval-hod-sun.pdf \
transits-milton_pandr_north-interval-hod-sun.pdf \
trips-milton_pandr_south-passenger_trip-hist.pdf \
trips-milton_pandr_north-passenger_trip-hist.pdf \
trips-milton_pandr_south-passenger_trip-moy-mon_fri.pdf \
trips-milton_pandr_north-passenger_trip-moy-mon_fri.pdf \
trips-milton_pandr_south-passenger_trip-moy-sat.pdf \
trips-milton_pandr_north-passenger_trip-moy-sat.pdf \
trips-milton_pandr_south-passenger_trip-moy-sun.pdf \
trips-milton_pandr_north-passenger_trip-moy-sun.pdf \
trips-milton_pandr_south-passenger_trip-dow.pdf \
trips-milton_pandr_north-passenger_trip-dow.pdf \
trips-milton_pandr_south-passenger_trip-hod-mon_fri.pdf \
trips-milton_pandr_north-passenger_trip-hod-mon_fri.pdf \
trips-milton_pandr_south-passenger_trip-hod-sat.pdf \
trips-milton_pandr_north-passenger_trip-hod-sat.pdf \
trips-milton_pandr_south-passenger_trip-hod-sun.pdf \
trips-milton_pandr_north-passenger_trip-hod-sun.pdf \
trips-milton_pandr_south-passenger_trip-example.pdf \
trips-milton_pandr_north-passenger_trip-example.pdf \
trips-milton_pandr_south-passenger_trip-overall.pdf \
trips-milton_pandr_north-passenger_trip-overall.pdf
