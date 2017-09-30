from django.contrib import admin
from bank.models import profile, Account, Loan, History, Action

admin.site.register(profile)
admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(History)
admin.site.register(Action)

