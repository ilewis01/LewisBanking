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

from bank.functions import fetchSecurityQuestions1, fetchSecurityQuestions2

from bank.models import profile, Account, Loan

def index(request):
	content = {}
	content['title'] = "Lewis Bank of CCNY"
	content.update(csrf(request))
	return render_to_response('index.html', content)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        profile = getAccount(user)

        if user.is_active == False:
        	return HttpResponseRedirect('/validationRequired/')
        else:
	        return HttpResponseRedirect('/home/')
    else:
        return HttpResponseRedirect('/invalid_login')

def newAccount(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | New Account"
	content['questions1'] = fetchSecurityQuestions1()
	content['questions2'] = fetchSecurityQuestions2()
	return render_to_response('newAccount.html', content)

def create_account(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | New Account"
	return render_to_response('create_account.html', content)

def newLoan(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | New Loan Application"
	return render_to_response('newLoan.html', content)

def complete_loan(request):
	content = {}
	content.update(csrf(request))
	content['title'] = "Lewis Bank | New Account"
	return render_to_response('complete_loan.html', content)

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







