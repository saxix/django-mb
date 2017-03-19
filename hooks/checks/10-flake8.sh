if git diff-index --quiet HEAD --; then
    # no changes between index and working copy; just run tests
    OUT=`flake8 src`
    RET=$?
else
    # Test the version that's about to be committed,
    # stashing all unindexed changes
    git stash -q --keep-index
#    FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -e '\.py$')
    FILES=$(gitflow_commit_files py)
    OUT=`flake8 $FILES`
    RET=$?
    git stash pop -q
fi

if [ $RET -eq 0 ];then
    gitflow_ok "Flake8 ok"
else
    gitflow_fail "Flake8 found some issues."
    echo "$OUT"
    exit $RET

fi
