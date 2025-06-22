# if macos: 
# brew install ghostscript
# if linux: 
# sudo apt-get install ghostscript

# check ghostscript exist
if ! command -v gs &> /dev/null; then
    echo "ghostscript could not be found"
    # install ghostscript
    SYSTEM_TYPE=$(uname)
    if [ "$SYSTEM_TYPE" == "Darwin" ]; then
        brew install ghostscript
    elif [ "$SYSTEM_TYPE" == "Linux" ]; then
        sudo apt-get install ghostscript
    fi
fi

# compress pdf
# parameters:
# -sDEVICE=pdfwrite: 指定输出为PDF
# -dCompatibilityLevel=1.4: 设置PDF兼容性级别为1.4
# -dPDFSETTINGS=/ebook: 设置PDF优化选项为ebook
# -dNOPAUSE -dQUIET -dBATCH: 不提示用户输入，批量处理
# -sOutputFile=compressed.pdf: 指定输出文件名
# gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=Tiankai-thesis-draft.pdf main.pdf

gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile="compressed.pdf" main.pdf
