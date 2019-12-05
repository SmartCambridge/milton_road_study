#!/bin/bash

# Collect graphs into one big file in a sane order

"/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py" \
-o graphs.pdf   --verbose                                      \
bus-hist.pdf \
drakewell-hist.pdf \
bus-minutes-overall.pdf \
drakewell-minutes-overall.pdf \
bus-minutes-tod.pdf \
drakewell-minutes-tod.pdf \
bus-minutes-dow.pdf \
drakewell-minutes-dow.pdf \
bus-minutes-month.pdf \
drakewell-minutes-month.pdf \
bus-count-overall.pdf \
drakewell-count-overall.pdf \
bus-count-tod.pdf \
drakewell-count-tod.pdf \
bus-count-dow.pdf \
drakewell-count-dow.pdf \
bus-count-month.pdf \
drakewell-count-month.pdf
