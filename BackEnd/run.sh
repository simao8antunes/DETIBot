#!/usr/bin/env bash

export $(xargs -0 -a "/proc/1/environ")
/usr/local/bin/python /root/test.py -p /root/data/skip.json