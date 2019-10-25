#!/bin/sh

trap "exit" INT TERM ERR
trap "kill 0" EXIT

tensorboard --logdir scratch --port 6006 &
python3 app.py &

wait
