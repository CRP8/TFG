#!/bin/bash

sudo hciconfig hci0 piscan

cd /home/pi/tfg

sudo python3 rfcomm-server.py
