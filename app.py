#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request, Response
import datetime
from decimal import *
from math import fsum
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

accounts = [
    {
        'id': 0,
        'name': u'David',
        'surname': u'Vélez',
        'product': u'Check Account',
        'balance': 10.05
    },
    {
        'id': 1,
        'name': u'Cristina',
        'surname': u'Junqueira',
        'product': u'Credit Card',
        'balance': 100.5
    },
    {
        'id': 2,
        'name': u'Edward',
        'surname': u'Wible',
        'product': u'Rewards Account',
        'balance': 1005.0
    }
]

#Making a new account
@app.route('/checks_and_balances/api/v1.0/new_account', methods=['POST'])
def create_account():
    """
    Makes a new account and adds it into the database.

    Args:
        - name (string - from the request): Account's owner name
        - surname (string - from the request): Account's owner lastname
        - product (string - from the request): Product name for that account
        - balance (float - from the request): Inicial balance for the account

    Response:
        - (json): Details from the recently created account
    """
    if not request.json or not 'name' in request.json:
        abort(400)
    account = {
        'id': accounts[-1]['id'] + 1, #last id + 1
        'name': request.json['name'],
        'surname': request.json['surname'],
        'product': request.json.get('product', ""),
        'balance': request.json.get('balance', 0.00)
    }

    accounts.append(account)

    return json.dumps({'New Account': account}, ensure_ascii=False), 201,  {'Content-Type': 'text/css; charset=utf-8'}

#Making a new transaction
@app.route('/checks_and_balances/api/v1.0/transaction', methods=['PUT'])
def make_transaction():
    """
    Makes deposit/withdrawal from an account and updates balance.

    Args:
        - account_id (int - from the request): account identifier for the trans.
        - transaction (string - from the request): either deposit or withdrawal
        - amount (float - from the request): amount from the transaction
    Response:
        - (json): new balance for the account
    """
    account_id = request.json['account_id']
    aux_account = [account for account in accounts if account['id'] == account_id]
    if len(aux_account) == 0:
        abort(404)
    account_balance = Decimal(aux_account[0].get('balance')).quantize(Decimal('0.00'))
    transaction = request.json['transaction']
    transaction_amount = Decimal(abs(request.json['amount'])).quantize(Decimal('0.00'))

    if not request.json:
        abort(400)
    if transaction not in ['withdrawal', 'deposit']:
        abort(400, f'Invalid transaction name: {transaction}')
    if transaction == 'withdrawal':
        transaction_amount = transaction_amount*-1

    # the user can't withdraw more than the account has
    validation_sum = (account_balance + transaction_amount).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    if validation_sum >= 0:
        for real_account in accounts:
            if real_account.get('id') == account_id:
                real_account['balance'] = round(float(validation_sum),2)
    else:
        abort(400, {'error':'Not enough funds for this transaction'})

    return json.dumps({f'{transaction.capitalize()} Done. New balance': str(validation_sum)}, ensure_ascii=False), 200


@app.route('/checks_and_balances/api/v1.0/account', methods=['POST'])
def get_account():
    """
    Gets the details from an account.

    Args:
        - id (int -  from request): identificator of the account
    Response:
        - (json): Details from an account, including balance.
    """
    account_id = request.json['id']
    account = [account for account in accounts if account['id'] == account_id]
    if len(account) == 0:
        abort(404, 'Account not found')

    return json.dumps(account[0], ensure_ascii=False), 200, {'Content-Type': 'text/css; charset=utf-8'}

@app.route('/checks_and_balances/health')
def health_check():
    """
    Checks the availability of the service.

    Response:
    - 'Alive' message and date from the server.
    """
    now = datetime.datetime.now()
    return make_response(jsonify({'Alive': f'{now.strftime("%Y-%m-%d %H:%M")}'}), 200)

@app.errorhandler(404)
def not_found(error):
    """
    Handles errors from the requests gotten from clients

    Args:
    - error(error): The error to be handled in the request

    Response:
    - (json): the error code and 'Resource not found message'
    """
    return make_response(jsonify({'error': 'Resource not found'}), 404)


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', threaded=True)
