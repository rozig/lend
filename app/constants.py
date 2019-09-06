from django.utils.translation import gettext as _


ACCOUNT_NUMBER_MAX = 9999999999
ACCOUNT_NUMBER_MIN = 1000000000

TRANSACTION_ID_MAX = 999999999999
TRANSACTION_ID_MIN = 100000000000

MESSAGES = {
    'NOT_FOUND': _('{} not found.'),
    'ACCOUNT_EXISTS': _('You already have an account.'),
    'ACCOUNT_DOES_NOT_EXIST': _('You don\'t have any account.'),
    'URL_PARAM_MISSING': _('URL Parameter is missing.'),
    'FIELD_REQUIRED': _('{} is required.'),
    'UNPAID_LOAN': _('You have unpaid loan.'),
    'NOT_LOAN_OWNER': _(
        'You\'re not a loan owner, you can\'t pay someone else\'s loan.'),
    'LOAN_ALREADY_PAID': _('Loan is already paid.'),
    'WRONG_LOAN_AMOUNT': _(
        'Your loan amount must be between $500.00 and $50,000.00.'),
    'WRONG_LOAN_LENGTH': _(
        'Your loan length must be between 6 months to 96 months.'),
    'NON_ELIGIBLE_REQUEST': _(
        'You\'re not eligible for this loan request. Please read our policy again.'),
    'WRONG_SCORE_TYPE': _('Lend score type is not correct.')
}
