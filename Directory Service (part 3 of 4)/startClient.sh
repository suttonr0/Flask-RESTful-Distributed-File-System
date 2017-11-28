#!/bin/bash

echo "Enter IP for the directory server and press enter"
read serverIP
echo "$serverIP is the IP" 

echo "Enter Port for the directory server and press enter"
read serverPort
echo "$serverPort is the Port" 

## $1 for first argument in commandline
python3 basicClient.py $serverIP $serverPort

