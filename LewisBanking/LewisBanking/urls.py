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
    url(r'^load_account_list/$', 'bank.views.load_account_list'),
    url(r'^withdraw/$', 'bank.views.withdraw'),
    url(r'^deposit/$', 'bank.views.deposit'),
    url(r'^transfer/$', 'bank.views.transfer'),
    url(r'^add_account/$', 'bank.views.add_account'),
    url(r'^delete_account/$', 'bank.views.delete_account'),
    url(r'^withdraw0/$', 'bank.views.withdraw0'),
    url(r'^deposit0/$', 'bank.views.deposit0'),
    url(r'^transfer0/$', 'bank.views.transfer0'),
    url(r'^add_account0/$', 'bank.views.add_account0'),
    url(r'^delete_account0/$', 'bank.views.delete_account0'),
    url(r'^view_history/$', 'bank.views.view_history'),
    url(r'^view_history0/$', 'bank.views.view_history0'),
    url(r'^account_search/$', 'bank.views.account_search'),
    url(r'^accountResults/$', 'bank.views.accountResults'),   
    url(r'^account_results_loader/$', 'bank.views.account_results_loader'),
    url(r'^final_a_loader/$', 'bank.views.final_a_loader'),
    url(r'^load_loan_list/$', 'bank.views.load_loan_list'),
    url(r'^make_payment/$', 'bank.views.make_payment'),
    url(r'^make_payment0/$', 'bank.views.make_payment0'),
    url(r'^view_loan_history/$', 'bank.views.view_loan_history'),
    url(r'^view_loan_history0/$', 'bank.views.view_loan_history0'),
    url(r'^view_Payment_dates0/$', 'bank.views.view_Payment_dates0'),
    url(r'^refinance/$', 'bank.views.refinance'),
    url(r'^refinance0/$', 'bank.views.refinance0'),
    url(r'^user_new_loan/$', 'bank.views.user_new_loan'),
    url(r'^user_new_loan0/$', 'bank.views.user_new_loan0'),
    url(r'^user_new_loan_complete/$', 'bank.views.user_new_loan_complete'),
    url(r'^refinanceload/$', 'bank.views.refinanceload'),
    url(r'^loadPaymentDates/$', 'bank.views.loadPaymentDates'),
    url(r'^loan_search/$', 'bank.views.loan_search'),
    url(r'^update_phone_loader/$', 'bank.views.update_phone_loader'),
    url(r'^update_phone/$', 'bank.views.update_phone'),
    url(r'^loadNewPassword/$', 'bank.views.loadNewPassword'),
    url(r'^t_history_list/$', 'bank.views.t_history_list'),
    url(r'^load_history_list/$', 'bank.views.load_history_list'),
    url(r'^commitDelete/$', 'bank.views.commitDelete'),
    url(r'^load_history_search/$', 'bank.views.load_history_search'),
    url(r'^pr0/$', 'bank.views.pr0'),
    url(r'^pr1/$', 'bank.views.pr1'),
    url(r'^pr2/$', 'bank.views.pr2'),
    url(r'^prSuccess/$', 'bank.views.prSuccess'),









)
