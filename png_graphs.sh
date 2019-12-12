#!/bin/bash

# Convert PDFs to PNGs as needed


pdftoppm bus-hist.pdf -singlefile -png bus-hist
pdftoppm drakewell-hist.pdf -singlefile -png drakewell-hist
pdftoppm bus-minutes-overall.pdf -singlefile -png bus-minutes-overall
pdftoppm drakewell-minutes-overall.pdf -singlefile -png drakewell-minutes-overall
pdftoppm bus-minutes-tod.pdf -singlefile -png bus-minutes-tod
pdftoppm drakewell-minutes-tod.pdf -singlefile -png drakewell-minutes-tod
pdftoppm bus-minutes-dow.pdf -singlefile -png bus-minutes-dow
pdftoppm drakewell-minutes-dow.pdf -singlefile -png drakewell-minutes-dow
pdftoppm bus-minutes-month.pdf -singlefile -png bus-minutes-month
pdftoppm drakewell-minutes-month.pdf -singlefile -png drakewell-minutes-month
pdftoppm bus-count-overall.pdf -singlefile -png bus-count-overall
pdftoppm drakewell-count-overall.pdf -singlefile -png drakewell-count-overall
