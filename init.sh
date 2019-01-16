#!/bin/bash

docker build --rm -t checks_and_balances:latest .
docker run -d -p 5000:5000 checks_and_balances:latest
