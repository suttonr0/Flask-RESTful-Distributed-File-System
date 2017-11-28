#!/bin/bash

echo "Enter Port for file server 2 and press enter"
read serverPort
echo "$serverPort is the port to be used" 

## $1 for first argument in commandline
python3 fileServer2.py $serverPort

