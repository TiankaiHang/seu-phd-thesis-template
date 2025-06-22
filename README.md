# phd-thesis

## Note

- 授权页模板要更新（模板中是新的）
- 校徽颜色是祖母绿

## Install the environment with docker

### build docker from `texlive/texlive:latest`

```bash
PAPER_DIR=$(pwd)
docker run -it -v ${PAPER_DIR}:/workdir texlive/texlive:latest
```

### Install fonts

```bash
bash scripts/install_fonts.sh 
```



## Install without docker (linux / wsl)

```bash
sudo apt update
sudo apt install texlive-full
sudo apt install texlive-xetex

sudo apt install texlive-lang-chinese
sudo apt install latex-cjk-all
```

## Build

```bash
bash scripts/build_scratch.sh 
```

or

```bash
xelatex main.tex && bibtex main && xelatex main.tex && xelatex main.tex
```