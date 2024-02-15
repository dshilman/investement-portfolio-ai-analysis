#!/bin/sh
sudo wget https://bootstrap.pypa.io/get-pip.py
sudo python3 ./get-pip.py
sudo dnf install cronie cronie-anacron
mkdir ~/tmp
cd investment-portfilio-ai-analysis
sudo TMPDIR=~/tmp/ python3 -m pip install -r requirements.txt --no-cache-dir