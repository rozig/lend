from django.contrib import admin

from app.models import (User, Account, Loan, LoanPayment, LoanProfile)

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(LoanPayment)
admin.site.register(LoanProfile)
