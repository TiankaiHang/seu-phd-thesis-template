#!/bin/bash

set -e

PAPER_DIR=$(pwd)
# if [[ "$(docker images -q texlive/texlive:latest 2> /dev/null)" == "" ]]; then
#     docker pull texlive/texlive:latest
# fi

cd ${PAPER_DIR}

# docker run --rm -it -v ${PAPER_DIR}:/workdir texlive/texlive:latest \
# /bin/bash -c "cd /workdir && xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex"

xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex

# compress pdf
bash scripts/compress_pdf.sh