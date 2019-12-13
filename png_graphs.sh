#!/bin/bash

# Convert PDFs to PNGs as needed

mkdir -p png

pdftoppm pdf/bus-hist.pdf -singlefile -png png/bus-hist
pdftoppm pdf/drakewell-hist.pdf -singlefile -png png/drakewell-hist
pdftoppm pdf/bus-minutes-overall.pdf -singlefile -png png/bus-minutes-overall
pdftoppm pdf/drakewell-minutes-overall.pdf -singlefile -png png/drakewell-minutes-overall
pdftoppm pdf/bus-minutes-tod.pdf -singlefile -png png/bus-minutes-tod
pdftoppm pdf/drakewell-minutes-tod.pdf -singlefile -png png/drakewell-minutes-tod
pdftoppm pdf/bus-minutes-dow.pdf -singlefile -png png/bus-minutes-dow
pdftoppm pdf/drakewell-minutes-dow.pdf -singlefile -png png/drakewell-minutes-dow
pdftoppm pdf/bus-minutes-month.pdf -singlefile -png png/bus-minutes-month
pdftoppm pdf/drakewell-minutes-month.pdf -singlefile -png png/drakewell-minutes-month
pdftoppm pdf/bus-count-overall.pdf -singlefile -png png/bus-count-overall
pdftoppm pdf/drakewell-count-overall.pdf -singlefile -png png/drakewell-count-overall
pdftoppm pdf/drakewell-count-month.pdf -singlefile -png png/drakewell-count-month
pdftoppm pdf/both-minutes-overall.pdf -singlefile -png png/both-minutes-overall
pdftoppm pdf/both-hist.pdf -singlefile -png png/both-hist