from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
import random
import json
import json as simplejson

from bank.models import profile, Account, Loan


def fetchSecurityQuestions1():
	questions = []

	for i in range(5):
		q = {}
		q['index'] = i
		questions.append(q)

	questions[0]['question'] = "What is your mother's maiden name?"
	questions[1]['question'] = "What high school did you attend?"
	questions[2]['question'] = "What is you maternal grandmother's name?"
	questions[3]['question'] = "What is you paternal grandmother's name?"
	questions[4]['question'] = "What is you maternal grandfather's name?"


	return questions

def fetchSecurityQuestions2():
	questions = []

	for i in range(5):
		q = {}
		q['index'] = i
		questions.append(q)

	questions[0]['question'] = "What is you paternal grandfather's name?"
	questions[1]['question'] = "What is the name of the street where you grew up?"
	questions[2]['question'] = "What is your favorite food?"
	questions[3]['question'] = "What is your childhood best friend's name?"
	questions[4]['question'] = "What is the name of your elementary school?"

	return questions