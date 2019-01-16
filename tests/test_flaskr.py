#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Funciones que toma pytest para evaluar la librería
"""
import os
import logging
import pytest
import sys
sys.path.append('./')


from werkzeug import exceptions
from datetime import datetime
from app import app
import tempfile

@pytest.fixture
def client():
    client = app.test_client()

    yield client


def test_create_accounts(client):
    """
    Test the creation of new accounts via the API call
    """
    request_test = client.post('/checks_and_balances/api/v1.0/new_account',
                                json={
                                      'name': 'Esteban',
                                      'surname': 'Díaz',
                                      'product': 'Awesome Account',
                                      'balance': 10000.05
                                      })

    wanted_result = {'New Account': {'id': 3, 'name': 'Esteban', 'surname': 'Díaz', 'product': 'Awesome Account', 'balance': 10000.05}}

    json_data = request_test.get_json(force=True)

    assert json_data['New Account'] == wanted_result['New Account']

def test_get_account(client):
    """
    Test for the obtention of the account given an id
    """
    request_test = client.post('/checks_and_balances/api/v1.0/account',
                                 json={'id': 0})
    json_data = request_test.get_json(force=True)

    wanted_result = {
        'id': 0,
        'name': u'David',
        'surname': u'Vélez',
        'product': u'Check Account',
        'balance': 10.05
    }

    assert json_data == wanted_result


def test_make_deposit(client):
    """
    Test for making deposit for a given account id
    """
    request_test = client.put('/checks_and_balances/api/v1.0/transaction',json=
    {
    "account_id": 2,
    "transaction": "deposit",
    "amount": 0.3
    })

    json_data = request_test.get_json(force=True)

    wanted_result = {"Deposit Done. New balance": "1005.30"}

    assert json_data == wanted_result

def test_make_withdrawal(client):
    """
    Test for a withdrawal for a given account
    """
    request_test = client.put('/checks_and_balances/api/v1.0/transaction',json=
    {
    "account_id": 1,
    "transaction": "withdrawal",
    "amount": 10.03
    })

    json_data = request_test.get_json(force=True)

    wanted_result = {"Withdrawal Done. New balance": "90.47"}

    assert json_data == wanted_result
