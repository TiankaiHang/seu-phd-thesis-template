# xelatex main.tex 
# bibtex  main
# xelatex main.tex
# xelatex main.tex

set -x

if [[ "$(docker images -q tiankaihang/latex:latest 2> /dev/null)" == "" ]]; then
    docker pull tiankaihang/latex:latest
fi

# PAPER_DIR=/home/t-thang/code_base/phd-thesis
# pwd
PAPER_DIR=$(pwd)
echo "PAPER_DIR: $PAPER_DIR"

docker run --rm -it -v ${PAPER_DIR}:/workdir tiankaihang/latex:latest \
    sh -c "cd /workdir && sh scripts/install_fonts.sh && xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex"  
