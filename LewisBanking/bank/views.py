from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.template.loader import get_template
from django.conf import settings
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import loader, Context
from datetime import datetime
from datetime import date
import json
import json as simplejson
from xhtml2pdf import pisa
from django.core import serializers
from django.http import FileResponse, Http404

from bank.functions import getUserProfile, fetch_content

from bank.models import profile, Account, Loan, History

def index(request):
	content = {}
	content['title'] = "Lewis Bank of CCNY"
	content.update(csrf(request))
	return render_to_response('index.html', content)

def auth_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        profile = getUserProfile(user)

        if user.is_active == False:
        	return HttpResponseRedirect('/validationRequired/')
        else:
	        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/invalid_login')

def newAccount(request):
	content = fetch_content(request, "newAccount_0")
	content.update(csrf(request))
	return render_to_response('newAccount.html', content)

def create_account(request):
	content = fetch_content(request, "newAccount_1")
	content.update(csrf(request))

	if content['created'] == True:
		return render_to_response('create_account.html', content)
	else:
		return render_to_response('complete_loan_exist.html', content)

def newLoan(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | New Loan Application"
	return render_to_response('newLoan.html', content)

def complete_loan(request):
	content = fetch_content(request, "newLoan_0")
	content.update(csrf(request))
	status = content['status']

	if status == 1:
		return render_to_response('complete_loan.html', content)
	elif status == 0:
		return render_to_response('complete_loan_exist.html', content)
	elif status == -1:
		return render_to_response('complete_loan_denied.html', content)

def loanCreated(request):
	content = fetch_content(request, "newLoan_1")
	content.update(csrf(request))
	return render_to_response('loan_created.html', content)

def validationRequired(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | Account Validation Required"
	return render_to_response('validationRequired.html')

def invalid_login(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | Invalid Login"
	return render_to_response('invalid_login.html')

@login_required(login_url='/index')
def logout(request):
	auth.logout(request)
	content = {}
	content.update(csrf(request))
	return render_to_response('logout.html', content)

@login_required(login_url='/index')
def home(request):
	content = fetch_content(request, "home")
	content.update(csrf(request))
	return render_to_response('home.html', content)

@login_required(login_url='/index')
def summary(request):
	content = fetch_content(request, "summary")
	content.update(csrf(request))
	return render_to_response('summary.html', content)

@login_required(login_url='/index')
def accounts(request):
	content = fetch_content(request, "accounts")
	content.update(csrf(request))
	return render_to_response('accounts.html', content)

@login_required(login_url='/index')
def loans(request):
	content = fetch_content(request, "loans")
	content.update(csrf(request))
	return render_to_response('loans.html', content)

@login_required(login_url='/index')
def transactions(request):
	content = fetch_content(request, "transactions")
	content.update(csrf(request))
	return render_to_response('transactions.html', content)

@login_required(login_url='/index')
def profile(request):
	content = fetch_content(request, "profile")
	content.update(csrf(request))
	return render_to_response('profile.html', content)

@login_required(login_url='/index')
def updatePassword(request):
	content = fetch_content(request, "password")
	content.update(csrf(request))
	return render_to_response('updatePassword.html', content)

@login_required(login_url='/index')
def deleteAccount(request):
	content = fetch_content(request, "delete")
	content.update(csrf(request))
	return render_to_response('deleteAccount.html', content)

@login_required(login_url='/index')
def load_sorted(request):
	content = fetch_content(request, "sorted")
	content.update(csrf(request))
	return render_to_response('load_sorted.html', content)

@login_required(login_url='/index')
def load_account_list(request):
	content = fetch_content(request, "account_list")
	content.update(csrf(request))
	return render_to_response('account_list.html', content)

@login_required(login_url='/index')
def withdraw(request):
	content = fetch_content(request, "profile")
	content.update(csrf(request))
	return render_to_response('withdraw.html', content)

@login_required(login_url='/index')
def deposit(request):
	content = fetch_content(request, "password")
	content.update(csrf(request))
	return render_to_response('deposit.html', content)

@login_required(login_url='/index')
def transfer(request):
	content = fetch_content(request, "delete")
	content.update(csrf(request))
	return render_to_response('transfer.html', content)

@login_required(login_url='/index')
def add_account(request):
	content = fetch_content(request, "sorted")
	content.update(csrf(request))
	return render_to_response('add_account.html', content)

@login_required(login_url='/index')
def delete_account(request):
	content = fetch_content(request, "account_list")
	content.update(csrf(request))
	return render_to_response('delete_account.html', content)








