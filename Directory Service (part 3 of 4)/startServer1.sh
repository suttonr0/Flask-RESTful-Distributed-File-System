#!/bin/bash

echo "Enter Port for file server 1 and press enter"
read serverPort
echo "$serverPort is the port to be used" 

## $1 for first argument in commandline
python3 fileServer1.py $serverPort

