from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
import random
import json
import json as simplejson
from bank.models import profile


def getAccount(request):
	no = None