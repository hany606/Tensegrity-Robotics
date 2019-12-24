#!/bin/bash
dir=$(dirname $0)/..

bash $dir/build.sh
bash $dir/build.sh
bash $dir/build.sh

bash $dir/bin/setup_gym_env.sh