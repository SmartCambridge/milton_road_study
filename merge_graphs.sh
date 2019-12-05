#!/bin/bash

# Collect graphs into one big file in a sane order

"/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py" \
-o graphs.pdf   --verbose                                      \
drakewell/drakewell-hist.pdf \
bus/bus-hist.pdf \
drakewell/drakewell-overall.pdf \
bus/bus-overall.pdf \
drakewell/drakewell-tod.pdf \
bus/bus-tod.pdf \
drakewell/drakewell-dow.pdf \
bus/bus-dow.pdf \
drakewell/drakewell-month.pdf \
bus/bus-month.pdf
