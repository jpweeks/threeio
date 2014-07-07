#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

source setup_test_env.bash
blender --background $BLEND/scene_spot_light.blend \
    --python $PYSCRIPT -- $TMP_JSON --vertices --faces --scene \
    --lights --materials
testjson $@ --tag $(tagname)
