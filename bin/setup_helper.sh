#!/bin/bash
dir=$(dirname $0)/../bin

bash $dir/build.sh
bash $dir/build.sh
bash $dir/build.sh

bash $dir/setup_gym_env.sh