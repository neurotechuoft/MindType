#!/usr/bin/env bash
source "MindType/bin/activate"
QT_X11_NO_MITSHM=1 python3 main.py -p /dev/ttyUSB0 --add pub_sub
