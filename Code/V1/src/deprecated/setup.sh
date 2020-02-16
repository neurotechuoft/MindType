#!/usr/bin/env bash
sudo apt-get install python3-dev python3-venv
python3 -m venv MindType
pip3 install -r requirements.txt
sudo bash -c 'echo KERNEL==\"ttyUSB[0-9]*\",NAME=\"tts/USB%n\",SYMLINK+=\"%k\",GROUP=\"uucp\",MODE=\"0666\" >> /etc/udev/rules.d/50-ttyusb.rules'
cd openbci_board
python3 setup.py build_ext --inplace
cd ..
