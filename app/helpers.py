import datetime
import random

from app.constants import (
    ACCOUNT_NUMBER_MAX, ACCOUNT_NUMBER_MIN, TRANSACTION_ID_MAX, TRANSACTION_ID_MIN, MESSAGES)
from app.models import Account, Transaction


def generate_account_number():
    number = random.randint(ACCOUNT_NUMBER_MIN, ACCOUNT_NUMBER_MAX)
    try:
        Account.objects.get(number=number)
        return generate_account_number()
    except Account.DoesNotExist:
        return number


def generate_transaction_id():
    _id = random.randint(ACCOUNT_NUMBER_MIN, ACCOUNT_NUMBER_MAX)
    try:
        Transaction.objects.get(id=_id)
        return generate_account_number()
    except Transaction.DoesNotExist:
        return _id


def is_eligible_lender(amount, length, score, num_of_loans):
    if amount > 50000 or amount < 500:
        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }

    if length > 96 or length < 6:
        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }

    if num_of_loans <= 5:
        return check_eligibility(amount, length, 'newbee')
    elif 5 < num_of_loans <= 10:
        _type = 'bronze' if 60 <= score else 'newbee'
        return check_eligibility(amount, length, _type)
    elif 10 < num_of_loans <= 25:
        _type = 'silver' if 120 <= score else 'bronze'
        return check_eligibility(amount, length, _type)
    else:
        _type = 'gold' if 180 <= score else 'silver'
        return check_eligibility(amount, length, _type)


def check_eligibility(amount, length, _type):
    if _type == 'newbee':
        if 500 <= amount <= 3000 and 6 <= length <= 24:
            interest_rate = 17
            if length <= 12:
                interest_rate += 18 / length
            else:
                interest_rate -= 18 / length

            return {
                'eligible': True,
                'interest_rate': interest_rate
            }

        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }
    elif _type == 'bronze':
        if 500 <= amount <= 10000 and 6 <= length <= 48:
            interest_rate = 14
            if length <= 24:
                interest_rate += 22 / length
            else:
                interest_rate -= 22 / length

            return {
                'eligible': True,
                'interest_rate': interest_rate
            }
        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }
    elif _type == 'silver':
        if 500 <= amount <= 30000 and 6 <= length < 72:
            interest_rate = 11
            if length <= 36:
                interest_rate += 34 / length
            else:
                interest_rate -= 34 / length

            return {
                'eligible': True,
                'interest_rate': interest_rate
            }
        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }
    elif _type == 'gold':
        if 500 <= amount <= 50000 and 6 <= length < 96:
            interest_rate = 8
            if length <= 48:
                interest_rate += 44 / length
            else:
                interest_rate -= 44 / length

            return {
                'eligible': True,
                'interest_rate': interest_rate
            }
        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }
    else:
        return {
            'eligible': False,
            'reason': MESSAGES.get('')
        }


def add_months(date, months):
    try:
        result = date.replace(day=1)
        result += datetime.timedelta(days=31)
        result.replace(day=date.day)
    except ValueError:
        result = date + datetime.timedelta(days=31)
        result.replace(day=1)
        result -= datetime.timedelta(days=1)

    return result
