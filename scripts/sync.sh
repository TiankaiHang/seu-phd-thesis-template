COMMENT="$1"

if [ -z "$COMMENT" ]; then
    COMMENT="sync"
fi

git pull

git add .
git commit -m "$COMMENT"
git push
