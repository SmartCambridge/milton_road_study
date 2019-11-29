#!/bin/bash

# Collect graphs into one big file in a sane order

"/System/Library/Automator/Combine PDF Pages.action/Contents/Resources/join.py" \
-o drakewell-graphs.pdf                                        \
drakewell-hist.pdf \
drakewell-moy-mon_fri.pdf \
drakewell-moy-sat.pdf \
drakewell-moy-sun.pdf \
drakewell-dow.pdf \
drakewell-hod-mon_fri.pdf \
drakewell-hod-sat.pdf \
drakewell-hod-sun.pdf \
drakewell-example.pdf \
drakewell-overall.pdf
