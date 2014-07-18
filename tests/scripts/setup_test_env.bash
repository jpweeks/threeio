#!/bin/bash

# you must have blender setup to run from the command line
if [[ `which blender` == "" ]]; then
    echo "No 'blender' executable found on the command line"
    exit 1
fi

export TMP_JSON=`python -c "import tempfile;print(tempfile.mktemp(prefix='$TAG.', suffix='.json'))"`

_dir=`dirname $DIR`
_dir=`dirname $_dir`
export BLENDER_USER_SCRIPTS="$_dir/BLENDER_USER_SCRIPTS"
unset _dir

# set the root for blend files
export BLEND=$(cd ../blend; pwd)

# set the python script to exec in batch
export PYSCRIPT='exporter.py'

# set the python script for running tests
export PYTEST='test.py'

function testjson() {
    python3 $DIR/test.py $TMP_JSON $@
}

function tagname() {
    tag=`basename $0`
    tag=${tag#test_}
    tag=${tag%%.*}
    echo $tag
}
