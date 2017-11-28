#!/bin/bash

echo "Enter Port for the Server and press enter"
read serverPort
echo "$serverPort is the port to be used" 

## $1 for first argument in commandline
python3 fileServer.py $serverPort

