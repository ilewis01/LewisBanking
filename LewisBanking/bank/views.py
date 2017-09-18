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

from bank.models import profile

def index(request):
	content = {}
	content['title'] = "Lewis Bank of CCNY"
	content.update(csrf(request))
	return render_to_response('index.html', content)
