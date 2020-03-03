#!/bin/bash

sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install virtualenv
sudo apt-get install python3-tk

virtualenv venv
source venv/bin/activate	
pip3 install -r requirements.txt
deactivate
