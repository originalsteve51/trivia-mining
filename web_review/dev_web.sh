#!/bin/zsh

export RUN_ON_HOST="localhost"
export USING_PORT=8081
export UPDATE_INTERVAL=1
export DEBUG_MODE=True

python -i setlist_web.py
