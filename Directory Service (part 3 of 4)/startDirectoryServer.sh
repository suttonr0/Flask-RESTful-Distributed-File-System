#!/bin/bash

echo "Enter IP for file server 1 and press enter"
read server1IP
echo "IP: $server1IP" 

echo "Enter Port for file server 1 and press enter"
read server1Port
echo "Port: $server1Port" 

echo "Enter IP for file server 2 and press enter"
read server2IP
echo "IP: $server2IP" 

echo "Enter Port for file server 2 and press enter"
read server2Port
echo "Port: $server2Port" 

echo "Enter Port the client should use to access the directory server"
read dirServerPort
echo "Port: $dirServerPort" 

## $1 for first argument in commandline
python3 directoryServer.py $server1IP $server1Port $server2IP $server2Port $dirServerPort

