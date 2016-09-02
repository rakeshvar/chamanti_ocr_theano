#! /bin/bash

echo "Installing system dependencies..."
sudo apt-get install libffi-dev

echo "Installing python packages..."
sudo pip3 install --upgrade pip
sudo pip3 install -r requirements.txt
