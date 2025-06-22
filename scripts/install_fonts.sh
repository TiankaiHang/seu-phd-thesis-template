fc-list :lang-zh

mkdir -p /usr/share/fonts/chinese

wget "https://github.com/TiankaiHang/storage-2024/releases/download/v2/simsun.ttc" -O /usr/share/fonts/chinese/simsun.ttc
wget "https://github.com/TiankaiHang/storage-2024/releases/download/v2/Times.New.Roman.ttf" -O "/usr/share/fonts/chinese/Times New Roman.ttf"
wget "https://github.com/TiankaiHang/storage-2024/releases/download/v2/FandolSong-Regular.otf" -O "/usr/share/fonts/chinese/FandolSong-Regular.otf"

# update cache
fc-cache -f -v

mkfontscale
mkfontdir

fc-list | grep SimSun
fc-list | grep Roman

# clean 
find . -type f \( -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.bbl" -o -name "*.blg" -o -name "*.synctex.gz" \) -delete