from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bank.views.index'),
    url(r'^index/$', 'bank.views.index'),
    url(r'^auth_view/$', 'bank.views.auth_view'),
     url(r'^logout/$', 'bank.views.logout'),
    url(r'^validationRequired/$', 'bank.views.validationRequired'),
    url(r'^invalid_login/$', 'bank.views.invalid_login'),
    url(r'^newAccount/$', 'bank.views.newAccount'),
    url(r'^newLoan/$', 'bank.views.newLoan'),
    url(r'^create_account/$', 'bank.views.create_account'),
    url(r'^complete_loan/$', 'bank.views.complete_loan'),
    url(r'^loanCreated/$', 'bank.views.loanCreated'),
    url(r'^home/$', 'bank.views.home'),
    url(r'^summary/$', 'bank.views.summary'),
    url(r'^accounts/$', 'bank.views.accounts'),
    url(r'^loans/$', 'bank.views.loans'),
    url(r'^transactions/$', 'bank.views.transactions'),
    url(r'^profile/$', 'bank.views.profile'),
    url(r'^updatePassword/$', 'bank.views.updatePassword'),
    url(r'^deleteAccount/$', 'bank.views.deleteAccount'),
    url(r'^load_sorted/$', 'bank.views.load_sorted'),
)
