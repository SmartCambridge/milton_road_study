#!/bin/bash

# Collect graphs into one big file in a sane order

"/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py" \
-o graphs.pdf                                        \
transits-milton_pandr_north-all_trip-hist.pdf        \
transits-milton_pandr_north-all_trip-moy-mon_fri.pdf \
transits-milton_pandr_north-all_trip-moy-sat_sun.pdf \
transits-milton_pandr_north-all_trip-dow.pdf         \
transits-milton_pandr_north-all_trip-hod-mon_fri.pdf \
transits-milton_pandr_north-all_trip-hod-sat_sun.pdf \
transits-milton_pandr_north-interval-hist.pdf        \
transits-milton_pandr_north-interval-moy-mon_fri.pdf \
transits-milton_pandr_north-interval-moy-sat_sun.pdf \
transits-milton_pandr_north-interval-dow.pdf         \
transits-milton_pandr_north-interval-hod-mon_fri.pdf \
transits-milton_pandr_north-interval-hod-sat_sun.pdf \
transits-milton_pandr_north-worst-hist.pdf           \
transits-milton_pandr_north-worst-moy.pdf            \
transits-milton_pandr_north-worst-dow.pdf            \
transits-milton_pandr_north-worst-hod.pdf            \
transits-milton_pandr_north-best_worst.pdf           \
transits-milton_pandr_south-all_trip-hist.pdf        \
transits-milton_pandr_south-all_trip-moy-mon_fri.pdf \
transits-milton_pandr_south-all_trip-moy-sat_sun.pdf \
transits-milton_pandr_south-all_trip-dow.pdf         \
transits-milton_pandr_south-all_trip-hod-mon_fri.pdf \
transits-milton_pandr_south-all_trip-hod-sat_sun.pdf \
transits-milton_pandr_south-interval-hist.pdf        \
transits-milton_pandr_south-interval-moy-mon_fri.pdf \
transits-milton_pandr_south-interval-moy-sat_sun.pdf \
transits-milton_pandr_south-interval-dow.pdf         \
transits-milton_pandr_south-interval-hod-mon_fri.pdf \
transits-milton_pandr_south-interval-hod-sat_sun.pdf \
transits-milton_pandr_south-worst-hist.pdf           \
transits-milton_pandr_south-worst-moy.pdf            \
transits-milton_pandr_south-worst-dow.pdf            \
transits-milton_pandr_south-worst-hod.pdf            \
transits-milton_pandr_south-best_worst.pdf           \
