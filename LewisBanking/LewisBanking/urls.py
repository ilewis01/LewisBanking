from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bank.views.index'),
    url(r'^index/$', 'bank.views.index'),
    url(r'^auth_view/$', 'bank.views.auth_view'),
    url(r'^validationRequired/$', 'bank.views.validationRequired'),
    url(r'^invalid_login/$', 'bank.views.invalid_login'),
    url(r'^newAccount/$', 'bank.views.newAccount'),
    url(r'^newLoan/$', 'bank.views.newLoan'),
    url(r'^create_account/$', 'bank.views.create_account'),
    url(r'^complete_loan/$', 'bank.views.complete_loan'),
    url(r'^loanCreated/$', 'bank.views.loanCreated'),
)
