# Checks and Balances

## What is Checks and Balances?
It's a service that lets create a new account, check the balance of the accounts in the system, and make transactions: deposits and withdrawals

## Are there any requirements to use it?
Yes, just a few*:

- Python >=3.6
- [Docker](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac)


\* It's recommended to be deployed on a Mac OS/Linux system.

## How can I deploy it?
To run it you need to run the command in the system's terminal:

```
$ chmod +x init.sh
$ ./init.sh
```

This will run the script to build, run and expose the service on container running in a Docker engine locally

To check if the deployment was successful you can make a request to it like this:

```
$ curl -i localhost:5000/checks_and_balances/health
```
if everything goes well you should see a message like this:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 29
Server: Werkzeug/0.14.1 Python/3.6.7
Date: Mon, 03 Dec 2018 22:09:45 GMT

{"Alive":"2018-12-03 22:09"}
```
## How can I use it?

There are mainly 3 requests to use the API:

You can check some examples importing the json file into Postman from the `/Postman documentation` folder

Here are described too:

- New Account [POST]: /checks_and_balances/api/v1.0/new_account

- Account Details [POST]: /checks_and_balances/api/v1.0/account

- Transactions [PUT]: /checks_and_balances/api/v1.0/transaction


Health check:
- Health check [GET]: /checks_and_balances/health

## Cleaning Up

To uninstall everything just run the command:
```
$ chmod +x unistall.sh
$ ./unistall.sh
```
