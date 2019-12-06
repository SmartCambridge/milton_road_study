Milton Road Traffic Study 2019
==============================

This study compares journey times for buses with journey times for
general traffic on Milton Road in Cambridge. It looks at in-bound
traffic during the morning peak (07:30 to 09:30) between the junction
with the A14 and the junction with Arbury Road and Union Lane. It is
based on traffic statistics for November 2018 to October 2019.

The software used to compile this report is available on GitHub at
https://github.com/SmartCambridge/milton_road_study

Data
====

Bus journey times
-----------------

Bus journey times are from the SmartCambridge data platform which
extracts them from real-time bus position information to measure traffic
speeds in Cambridge. Journey times are extracted for buses travelling
through 'Zones' enclosing sections of road. For this study a custom zone
'milton_road_alternate_in' was defined for the section of Milton Road
between its junction with the A14 and its junction with Arbury Road and
Union Lane and journey times were extracted for it.

[Drafting note: this document currently quotes data from the related
zone 'milton_road_2_in' pending extraction of data for
'milton_road_alternate_in']

For comparability for other data, bus journey times were aggregated to
give median journey times for 15 minuite periods from 07:30 to 09:30.
This yielded 2026 samples with at least one journey out of a theoretical
maximum of about 2080 (52 weeks, 5 days per week, 8 samples per day),
containing a median of 4 journeys each (inter-quartile range 3 to 5).
The mean distance travelled by buses in this zone was 1578 meters.

General traffic journey Times
-----------------------------

Journey times for general traffic are from a realtime data platform
provided to the County Council by Drakewell Ltd. This uses information
broadcast by BlueTooth devices (mainly mobile phones) to measure journey
times between monitoring stations. There are about 40 such stations at
major junctions in Cambridge. This study used data from stations
MACSSL210023 (at the A14), MACSSL208512 (at the junction with Kings
Hedges Road) and MACSSL208513 (at the junction with Milton Road and
Union Lane) covering a total distance of 2186 meters.

This study used archive data provided by Drakewell that gives median
journey times and number of journeys for 15 minuite intervals for
'Links' between pairs of stations. For the purposes of this study the
journey times on the two links were added to give total journey times.
Samples with less than 10 journeys on either link were omitted, leaving
a total of 1776 samples out of the theoretical maximum of about 2080.

The Drakewell data is sensitive to various configuration parameters
which are changed from time to time. Overall the samples contain a
median of 42 samples each (inter-quartile range 33 to 50), but there was
a noticeable drop in sample size in July 2019, from a median of about 45
to about 30, probably as a result of the 'outlier sensitivity removal'
parameter being increased to its maximum value. This does not appear to
have had much is any effect on the overall journey times reported.

Conclusions
===========

See attached graphs. Journey times vary widely, making them difficult to
summarise. Most of the attached graphs use a 'box and whisker'
representation in which the green line is the median, the box represents
the range from the 25th to the 75th percentile, and the whiskers the
range from the 1st to the 99th percentile (i.e. 98% of all
journeys). The black circles represent the remaining 2% of journeys.

1. Bus journeys are typically faster (median 4 minutes) than general traffic
journeys (meadian 6 minutes). They are also less variable (interquartile
range 3.8-4.8, maximum 9 vs. interquartile range 5.2-7.5, maximum 13.5).

2. All journey times vary very little by time of day or month. Bus
journey times vary very little by day of week but general traffic journeys
are slightly faster at the start and end of the week and slightly slower
on mid-week. This is consistent with traffic volumes observed
elsewhere which typically peak on Wednesdays.

3. While rare, all 'worst case' journey times can easily be double the
median time, sometimes more.
