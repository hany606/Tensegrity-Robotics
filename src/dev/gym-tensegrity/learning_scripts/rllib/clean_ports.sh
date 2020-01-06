#!/bin/bash

kill $(lsof -t -i:10042)
echo "Kill process of port 10042"
kill $(lsof -t -i:10043)
echo "Kill process of port 10043"
