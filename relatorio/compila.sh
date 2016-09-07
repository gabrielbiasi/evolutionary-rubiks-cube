#!/bin/bash

####
# Variables
####
NAME="tp-natural"

####
# Compiling
####
pdflatex -synctex=1 -interaction=nonstopmode -draftmode $NAME.tex
bibtex $NAME.aux
pdflatex -synctex=1 -interaction=nonstopmode -draftmode $NAME.tex
pdflatex -synctex=1 -interaction=nonstopmode $NAME.tex

####
# Removing aux files
###
rm $NAME.out $NAME.bbl $NAME.aux $NAME.blg $NAME.synctex.gz $NAME.log
