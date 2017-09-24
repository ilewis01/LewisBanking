from django.contrib import admin
from bank.models import profile, Account, Loan

admin.site.register(profile)
admin.site.register(Account)
admin.site.register(Loan)
