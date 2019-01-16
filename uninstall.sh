#!/bin/bash

docker rm $(docker stop $(docker ps -a -q --filter ancestor=checks_and_balances:latest --format="{{.ID}}"))
docker rmi checks_and_balances 
