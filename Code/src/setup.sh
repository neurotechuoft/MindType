#!/usr/bin/env bash
sudo bash -c 'echo KERNEL=="ttyUSB[0-9]*",NAME="tts/USB%n",SYMLINK+="%k",GROUP="uucp",MODE="0666" >> /etc/udev/rules.d/50-ttyusb.rules'
