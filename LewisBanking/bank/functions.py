from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import random
import json
import json as simplejson
from decimal import Decimal

from bank.models import profile, Account, Loan, History, Action


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

	questions[0]['question'] = "What is your favorite food"
	questions[1]['question'] = "What is the name of the street where you grew up?"
	questions[2]['question'] = "What is you paternal grandfather's name?"
	questions[3]['question'] = "What is your childhood best friend's name?"
	questions[4]['question'] = "What is the name of your elementary school?"

	return questions

def convert_month_toString(mm):
	if mm == 1:
		mm = "January"
	elif mm == 2:
		mm = "February"
	elif mm == 3:
		mm = "March"
	elif mm == 4:
		mm = "April"
	elif mm == 5:
		mm = "May"
	elif mm == 6:
		mm = "June"
	elif mm == 7:
		mm = "July"
	elif mm == 8:
		mm = "August"
	elif mm == 9:
		mm = "September"
	elif mm == 10:
		mm = "October"
	elif mm == 11:
		mm = "November"
	elif mm == 12:
		mm = "December"
	return mm

def convert_str_toDate(value):
	value = str(value)
	size = len(value)
	date = None
	count = 0
	temp = ""
	yy = ""
	mm = ""
	dd = ""

	for i in range(size):
		c = str(value[i])
		if c != "-":
			temp += c
		else:
			if count == 0:
				yy = temp
				temp = ""
				count += 1
			elif count == 1:
				mm = temp
				temp = ""
				count += 1
	dd = temp
	yy = int(yy)
	mm = int(mm)
	dd = int(dd)
	date = datetime(yy, mm, dd).date()
	return date


def fetchActions():
	actions = []
	action.append('Opened Account')
	action.append('Withdrawal')
	action.append('Deposit')
	action.append('Transfer From Account')
	action.append('Closed Account')
	action.append('Loan Approved')
	action.append('Payment')
	action.append('Refinanced Loan')
	action.append('Loan Default')
	action.append('Loan Default')
	action.append('Transfer To Account')
	return action

def get_action_from_text(action):
	actions = Action.objects.all()
	result = None

	for a in actions:
		if action == a.action:
			result = a
			break
	return result

def get_action_from_index(index):
	actions = Action.objects.all()
	result = None

	for a in actions:
		if index == a.index:
			result = a
			break
	return result

def format_currency(value):
	result = ""
	value = str(value)
	mix = value.split('.')
	dollars = str(mix[0])
	d_size = len(dollars)
	temp = ""

	for i in range(d_size):
		if i != 0 and (d_size - i) % 3 == 0:
			temp += ","
		temp += dollars[i]
	
	if len(mix) == 1:
		result = temp + ".00"
	elif len(mix) == 2:
		cents = str(mix[1])
		if len(cents) == 1:
			result = temp + "." + cents + "0"
		else:
			result = temp + "." + cents
	elif len(mix) == 1 and dollars == "0":
		result = 0

	return result


def userExist(email):
	exist = False
	users = User.objects.all()

	for u in users:
		if str(u.email) == str(email):
			exist = True
			break

	return exist

def full_user_match_request(request):
	fname = str(request.POST.get('fname'))
	lname = str(request.POST.get('lname'))
	email = str(request.POST.get('email'))
	phone = decodePhone(request)

	users = User.objects.all()
	test = {}
	test['exist'] = False
	test['user'] = None

	for u in users:
		pfile = getUserProfile(u)
		if str(u.first_name)==fname and str(u.last_name)==lname and str(u.email)==email and str(pfile.phone)==phone:
			test['exist'] = True
			test['user'] = u
			break
	return test

def getUserProfile(user):
	pfile = None
	profiles = profile.objects.all()

	for p in profiles:
		if p.user == user:
			pfile = p
			break
	return pfile

def locate_account(account_number):
	account = None
	a_list  = Account.objects.all()

	for a in a_list:
		if str(a.account_number) == account_number:
			account = a
			break
	return account

def newUser_account(request):
	content = {}
	content['created'] = False

	email = str(request.POST.get('email'))
	content['email'] = email

	if userExist(email) == False:
		content['created'] = True
		user = User()

		user.first_name = request.POST.get('fname')
		user.last_name = request.POST.get('lname')
		user.email = email
		user.username = email
		user.set_password(request.POST.get('password1'))
		user.save()

		profile = newProfile(request, user)
		account = newAccount(request, user.id)

		history = History(account_number=account.account_number)
		history.user_id = user.id
		history.account_type = get_account_type_text(account.isSavings)
		history.b_balance = 0.00
		history.e_balance = account.balance
		history.date = datetime.now().date()
		history.description = "Account Opened"
		history.action = get_action_from_index(0)

		profile.accounts = str(account.id) + "~"
		profile.is_active = True
		profile.save()
		account.save()
		history.save()

		content['user'] = user
		content['profile'] = profile
		content['account'] = account

	return content

def clear_format(value):
	value = str(value)
	result = ''
	for v in value:
		if v != ",":
			result += v
	return Decimal(result)

def buildLoan_init(request):
	content = {}
	content['title'] 	= "Lewis Bank | New Loan Application"

	fname = request.POST.get('fname')
	lname = request.POST.get('lname')
	email = request.POST.get('email')
	passw = str(request.POST.get('password1'))
	term  = request.POST.get("term")
	dates = loanDates_newLoan(term)
	loan_type = str(request.POST.get("ltype"))
	rate = str(request.POST.get("rate"))
	rate = Decimal(rate)
	rate /= 100

	content['loan_type'] = loan_type

	principal = str(request.POST.get("principal"))
	interest = str(request.POST.get("interest"))
	payment = str(request.POST.get("payments"))
	principal = clear_format(principal)
	interest = clear_format(interest)
	payment = clear_format(payment)
	total = principal + interest

	user = User()
	user.first_name = fname
	user.last_name = lname
	user.email = email
	user.username = email
	user.set_password(passw)
	user.save()

	pfile = profile(user=user)
	pfile.phone 		= request.POST.get("phone")
	pfile.question1 	= request.POST.get("security1")
	pfile.question2 	= request.POST.get("security2")
	pfile.answer1 		= request.POST.get("answer1")
	pfile.answer2 		= request.POST.get("answer2")
	pfile.recoveryCode 	= generateRandom(6, True, True)
	pfile.is_active 	= True

	loan = Loan(user_id=user.id)
	loan.account_number = fetchAccountNumber(8, True, True, "loan")
	loan.loan_amount 	= clear_format(principal)
	loan.balance 		= clear_format(request.POST.get("total"))
	loan.rate 			= rate
	loan.total_interest = interest
	loan.loan_type 		= enumerateLoanType(loan_type)
	loan.payment 		= clear_format(payment)
	loan.term 			= term
	loan.start_date 	= dates['start']
	loan.end_date 		= dates['end']
	loan.save()

	account = Account(user_id=user.id)
	account.account_number 	= fetchAccountNumber(8, False, True, "account")
	account.isSavings 		= pythonBool(request.POST.get("account_type"))
	account.balance 		= clear_format(request.POST.get("principal"))
	account.date 			= dates['start']
	account.save()

	encode = str(account.id) + "~" + str(loan.id) + "~"
	pfile.accounts = encode
	pfile.save()

	history_account 				= History()
	history_account.date 			= dates['start']
	history_account.account_type	= get_account_type_text(account.isSavings)
	history_account.user_id			= user.id
	history_account.description 	= "Loan " + str(loan.account_number) + " of $" + str(loan.loan_amount) + " deposited into new account"
	history_account.account_number	= account.account_number
	history_account.b_balance 		= 0
	history_account.e_balance 		= account.balance
	history_account.action 			= get_action_from_index(0)
	history_account.save()

	a_type = "Checking"

	if account.isSavings == True:
		a_type = "Savings"

	history_loan 	 				= History()
	history_loan.date 				= dates['start']
	history_loan.account_type		= "Loan"
	history_loan.user_id			= user.id
	history_loan.description 		= "Loan Approved and deposited into " + a_type + ": " + str(account.account_number)
	history_loan.account_number		= loan.account_number
	history_loan.e_balance 			= loan.balance
	history_loan.b_balance 			= 0
	history_loan.action 			= get_action_from_index(5)
	history_loan.save()

	content['format'] = format_currency(principal)
	content['user'] = user
	content['profile'] = profile
	content['account'] = account
	content['loan'] = loan
	return content

def newLoanDecision(request):
	content = {}
	content['title'] 	= "Lewis Bank | Loans"
	content['fname'] 	= request.POST.get("fname")
	principal 			= decoderCurrency(request, "dollars", "cents")
	content['amount'] 	= principal
	decision 			= creditCheck()

	if decision['decision'] == True:
		email = request.POST.get("email")
		content['email'] = email

		if userExist(email) == False:
			term 				= str(request.POST.get("loanTerm"))
			term 				= Decimal(term)
			rate				= decision['interest']
			monthly_payment		= calculatePayments(rate, term, principal)
			monthly_interest 	= monthly_payment - (principal/term)
			total_interest		= monthly_interest * term
			total 				= principal + total_interest

			monthly_payment		= format(monthly_payment, '.2f')
			monthly_interest	= format(monthly_interest, '.2f')
			total_interest		= format(total_interest, '.2f')
			total				= format(total, '.2f')
			term 				= int(term)
			rate 				= int(rate * 100)

			content['status'] 		= 1
			content['rate'] 		= rate
			content['term'] 		= term
			content['principal']	= format_currency(principal)
			content['payments'] 	= format_currency(monthly_payment)
			content['interest']		= total_interest
			content['total']		= format_currency(total)

			content['type'] 	= request.POST.get("loanType")
			content['lname'] 	= request.POST.get("lname")
			content['phone']	= decodePhone(request)
			content['dates']	= loanDates_newLoan(term)

			content['security1'] = fetchSecurityQuestions1()
			content['security2'] = fetchSecurityQuestions2()
		else:
			content['status'] 	= 0
	else:
		content['status'] 		= -1
	return content

def name_abv(user):
	name = str(user.first_name)
	name = name[0] + ". " + str(user.last_name)
	return name

def welcome_content(request):
	content= {}
	user = request.user
	name = name_abv(user)
	content['name'] = name
	content['user'] = user
	content['title'] = "Welcome to Lewis Bank"
	return content

def fetchAccountSummary(request):
	content = {}
	user = request.user
	name = name_abv(user)
	content['name'] = name
	content['user'] = user
	content['title'] = "Welcome to Lewis Bank"
	return content

def fetch_sorted_content(request):
	content = {}
	user = request.user
	sort = request.POST.get('sort')
	sorted_list = None
	direction = None

	if sort == None:
		sort = "date"
		direction = "descend"
	else:
		direction = str(request.POST.get("direction"))

	sorted_list = full_sort(user, sort, direction)

	content['direction'] = direction
	content['sort'] = sort
	content['sorted_list'] = sorted_list
	content['title'] = "Lewis Bank | Summary"
	return content

def fetchAccountContent(request):
	content = {}
	years = []
	days_from = []
	days_to = []
	months = []
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)
	today = datetime.now()

	# dates = fetch_date_ranges(user)

	yy_joined = user.date_joined.year
	mm_joined = user.date_joined.month
	dd_joined = user.date_joined.day
	yy = today.year
	mm = today.month
	dd = today.day 

	if yy - yy_joined == 0:
		years.append(yy)

		for i in range(mm - mm_joined + 1):
			d = {}
			d['value'] = mm_joined
			d['option'] = convert_month_toString(mm_joined)
			months.append(d)
			mm_joined += 1
	else:
		for j in range(yy - yy_joined + 1):
			years.append(yy_joined)
			yy_joined += 1

		for k in range(12):
			d = {}
			tm = k + 1
			d['value'] = tm
			d['option'] = convert_month_toString(tm)
			months.append(d)

	num_days_fm = getDays(mm_joined, yy_joined)
	num_days_to = getDays(mm, yy)

	for l in range(num_days_fm):
		days_from.append(l + 1)

	for m in range(num_days_to):
		days_to.append(m + 1)

	content['joined'] = dd_joined
	content['years'] = json.dumps(years)
	content['months'] = json.dumps(months)
	content['days_from'] = json.dumps(days_from)
	content['days_to'] = json.dumps(days_to)
	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Manage Accounts"
	return content

def getDays(mm, yy):
	days = 0
	if mm == 2:
		days = 28
		if yy % 4 == 0:
			days = 29
	elif mm == 4 or mm == 6 or mm == 9 or mm == 11:
		days = 30
	else:
		days = 31
	return days

def fetchLoansContent(request):
	content = {}
	years = []
	days_from = []
	days_to = []
	months = []
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)
	today = datetime.now()

	# dates = fetch_date_ranges(user)

	yy_joined = user.date_joined.year
	mm_joined = user.date_joined.month
	dd_joined = user.date_joined.day
	yy = today.year
	mm = today.month
	dd = today.day 

	if yy - yy_joined == 0:
		years.append(yy)

		for i in range(mm - mm_joined + 1):
			d = {}
			d['value'] = mm_joined
			d['option'] = convert_month_toString(mm_joined)
			months.append(d)
			mm_joined += 1
	else:
		for j in range(yy - yy_joined + 1):
			years.append(yy_joined)
			yy_joined += 1

		for k in range(12):
			d = {}
			tm = k + 1
			d['value'] = tm
			d['option'] = convert_month_toString(tm)
			months.append(d)

	num_days_fm = getDays(mm_joined, yy_joined)
	num_days_to = getDays(mm, yy)

	for l in range(num_days_fm):
		days_from.append(l + 1)

	for m in range(num_days_to):
		days_to.append(m + 1)

	content['joined'] = dd_joined
	content['years'] = json.dumps(years)
	content['months'] = json.dumps(months)
	content['days_from'] = json.dumps(days_from)
	content['days_to'] = json.dumps(days_to)
	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Manage Loans"
	return content

def fetchTransactionsContent(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)
	dates = fetch_date_ranges(user)

	content['day'] = dates['day']
	content['years'] = dates['years']
	content['months'] = dates['months']
	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Transaction History"
	return content

def fetchProfileContent(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

	content['name'] = name
	content['since'] = user.date_joined.date()
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Edit Profile"
	return content

def fetchPasswordContent(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Update Password"
	return content

def loadNewPassword(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)
	old = str(request.POST.get('old'))

	if user.check_password(old) == True:
		password = str(request.POST.get('password1'))
		user.set_password(password)
		user.save()
		update_session_auth_hash(request, user)

	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Update Password"
	return content

def fetchDeleteContent(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Delete Account"
	return content

def generateLoanTermHTML(rate, amount, loan_type, term):
	html = ""
	return html

def newProfile(request, user):
	pfile = profile()
	pfile.user = user
	pfile.phone = decodePhone(request)
	pfile.recoveryCode = generateRandom(6, True, True)
	pfile.question1 = request.POST.get("security1")
	pfile.question2 = request.POST.get("security2")
	pfile.answer1 = request.POST.get("answer1")
	pfile.answer2 = request.POST.get("answer2")
	return pfile

def newAccount(request, user_id):
	account = Account(user_id=user_id)
	account.account_number = fetchAccountNumber(8, False, True, "account")
	account.isSavings = pythonBool(request.POST.get("accountType"))
	account.balance = decoderCurrency(request, "dollars", "cents")
	account.date = datetime.now().date()
	return account


def pythonBool(value):
	if str(value) == "True":
		value = True
	else:
		value = False
	return value

def decoderCurrency(request, dollar_id, cents_id):
	result = None
	dollars = str(request.POST.get(dollar_id))
	dollars = Decimal(dollars)
	cents = "0." + str(request.POST.get(cents_id))
	cents = Decimal(cents)
	return dollars + cents


def decodePhone(request):
	phone1 = str(request.POST.get("phone1"))
	phone2 = str(request.POST.get("phone2"))
	phone3 = str(request.POST.get("phone3"))
	return "(" + phone1 + ") " + phone2 + "-" + phone3

def generateRandom(size, allowText, allowNumbers):
	code = ""
	pool = None

	if allowText == True and allowNumbers == False:
		pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	elif allowText == False and allowNumbers == True:
		pool = "0123456789"
	else:
		pool = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	for i in range(size):
		code += random.choice(pool)

	return code

def verifyAccountNumber(account_number, m_type):
	exist = False
	m_list = None

	if m_type == "account":
		m_list = Account.objects.all()
	elif m_type == "loan":
		m_list = Loan.objects.all()

	for t in m_list:
		if str(t.account_number) == account_number:
			exist = True
			break
	return exist

def fetchAccountNumber(size, allowText, allowNumbers, m_type):
	exist = True
	account_number = None

	while exist == True:
		account_number = generateRandom(size, allowText, allowNumbers)
		exist = verifyAccountNumber(account_number, m_type)

	return account_number

def creditCheck():
	loan = {}
	loan['decision'] = False
	loan['interest'] = 0

	decision = random.randrange(0, 2)

	if decision == 1:
		loan['decision'] = True
		index = random.randrange(0, 5)
		rates = []
		rates.append(0.01)
		rates.append(0.02)
		rates.append(0.03)
		rates.append(0.04)
		rates.append(0.05)
		loan['interest'] = rates[index]

	return loan

def newInterestRate():
	index = random.randrange(0, 5)
	rates = []
	rates.append(0.01)
	rates.append(0.02)
	rates.append(0.03)
	rates.append(0.04)
	rates.append(0.05)
	return rates[index]

def loanDates_newLoan(term):
	data = {}
	term = int(term) + 1
	start_date = datetime.now()
	end_date = start_date + relativedelta(months=+term)
	start_date = start_date.date()
	end_date = end_date.date()
	data['start'] = start_date
	data['end'] = end_date
	return data

def enumerateLoanType(loan_type):
	result = 0;

	if loan_type == "Personal":
		result = 1
	elif loan_type == "Business":
		result = 2
	elif loan_type == "Student":
		result == 3

	return result

def denumerateLoanType(loan_type):
	result = ""

	if loan_type == 1:
		result = "Personal"
	elif loan_type == 2:
		result = "Business"
	elif loan_type == 3:
		result = "Student"

	return result

def calculatePayments(rate, term, principal):
	rate = Decimal(rate)
	principal = Decimal(principal)
	term = Decimal(term)
	x1 = (1 + rate)**term
	numerator = x1 * rate
	denominator = x1 - 1
	division = numerator / denominator
	payments = principal * division
	return payments

def serialize_json(model, m_type):
	data = None
	if m_type == "History":
		data = json_dump_history(model)
	elif m_type == "Loan":
		data = json_dump_loans(model)
	elif m_type == "Account":
		data = json_dump_accounts(model)
	return data

def json_dump_accounts(account):
	data = {}
	fields = None
	data['user_id'] = account.user_id
	data['account_number'] = account.account_number
	data['isSavings'] = account.isSavings
	data['balance'] = str(account.balance)
	data['date'] = str(account.date)
	fields = json.dumps(data)
	return fields

def json_dump_loans(loan):
	data = {}
	fields = None
	data['user_id'] = loan.user_id
	data['account_number'] = loan.account_number
	data['principal'] = str(loan.loan_amount)
	data['balance'] = str(loan.balance)
	data['rate'] = str(loan.rate)
	data['total_interest'] = str(loan.total_interest)
	data['payment'] = str(loan.payment)
	data['loan_type'] = loan.loan_type
	data['term'] = loan.term
	data['start_date'] = str(loan.start_date)
	data['end_date'] = str(loan.end_date)
	fields = json.dumps(data)
	return fields

def json_dump_history(history):
	data = {}
	fields = None
	data['user_id'] = history.user_id
	data['account_number'] = history.account_number
	data['description'] = history.description
	data['balance'] = str(history.balance)
	data['date'] = str(history.date)
	data['account_type'] = history.account_type
	fields = json.dumps(data)
	return fields

def mega_account_link(h_list):
	data = []
	a_list = None

	for h in h_list:
		d = {}
		d['history'] = serialize_json(h, "History")
		a_type = str(h.account_type)

		if a_type == "Account":
			a_list = Account.objects.all()
		elif a_type == "Loan":
			a_list = Loan.objects.all()

		for a in a_list:
			if str(a.account_number) == str(h.account_number):
				dump = serialize_json(a, str(a.serializer))
				d['account'] = dump
				break
		data.append(d)
	return data


def mega_history_link(m_list):
	data = []
	h_list = History.objects.all()

	for m in m_list:
		d = {}
		d['account'] = serialize_json(m, str(m.serializer))
		d['history'] = []

		for h in h_list:
			if str(m.account_number) == str(h.account_number):
				dump = serialize_json(h, "History")
				d['history'].append(dump)
				break
		data.append(d)
	return data

def mega_account_sort(user, sort, direction, m_type):
	account_list = []
	m_list = None
	user_id = str(user.id)

	if direction == "descend":
		sort = "-" + sort

	if m_type == "Account":
		m_list = Account.objects.all().order_by(sort)
	elif m_type == "Loan":
		m_list = Loan.objects.all().order_by(sort)

	for m in m_list:
		if str(m.user_id) == user_id:
			account_list.append(m)

	sorted_list = mega_history_link(account_list)
	return sorted_list

def mega_sort(user, sort, direction, m_type):
	sorted_list = []

	if m_type == "Account" or m_type == "Loan":
		sorted_list = mega_account_sort(user, sort, direction, m_type)
	elif m_type == "History":
		sorted_list = mega_history_sort(user, sort, direction)

	return sorted_list

def mega_history_sort(user, sort, direction):
	data = []
	user_id = str(user.id)

	if direction == "descend":
		sort = "-" + sort

	h_list = History.objects.all().order_by(sort)

	for h in h_list:
		if str(h.user_id) == user_id:
			data.append(h)

	sorted_list = mega_account_link(data)
	return sorted_list

def full_sort(user, sort, direction):
	data = []
	user_id = str(user.id)

	if direction == "descend":
		sort = "-" + sort

	h_list = History.objects.all().order_by(sort)

	for h in h_list:
		if str(h.user_id) == user_id:
			data.append(h)

	sorted_list = mega_account_link_raw(data)
	return sorted_list

def single_history_link(account):
	history = None
	h_list = History.objects.all()

	for h in h_list:
		if str(h.account_number) == str(account.account_number):
			history = h
			break;
	return history

def get_all_history(account, sort, direction):
	history = []

	if direction == "descend":
		sort = "-" + sort

	h_list = History.objects.all().order_by(sort)

	for h in h_list:
		if str(h.account_number) == str(account.account_number):
			history.append(h)
	return history

def singleHistorySortOptions():
	options = []
	options.append('date')
	options.append('description')
	options.append('balance')
	options.append('action')
	return options

def fetch_account_history(request):
	content = {}
	h_list = []
	account_number = str(request.POST.get('account_number'))
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))
	m_sort = sort
	count = 0
	type = None

	if (direction == "descend"):
		m_sort = "-" + sort

	history = History.objects.all().order_by(m_sort)

	for h in history:
		if str(h.account_number) == account_number:
			d = {}

			if count == 0:
				m_type = h.account_type

			if count % 2 == 0:
				d['class'] = 'hi_clear'
			else:
				d['class'] = "hi_shade"

			d['history'] = h
			d['starting_balance'] = format_currency(h.b_balance)
			d['ending_balance'] = format_currency(h.e_balance)
			h_list.append(d)
			count += 1

	content['m_type'] = m_type
	content['sort'] = sort
	content['direction'] = direction
	content['account_number'] = account_number
	content['history'] = h_list;
	return content

def account_data_items(account, index):
	data = {}
	data['account'] = account

	if index == 0:
		data['class'] = "li_highlight"
	elif index % 2 == 0:
		data['class'] = "li_clear"
	else:
		data['class'] = "li_shade"

	data['type'] = get_account_type_text(account.isSavings)
	data['index'] = index
	data['balancef'] = format_currency(account.balance)
	return data

def advanced_account_search(accounts, search, search2, method, user_id):
	data = []
	count = 0

	if str(method) == 'money':
		fm_search = Decimal(str(search))
		to_search = Decimal(str(search2))

		for a in accounts:
			if str(user_id) == str(a.user_id):
				if a.balance >= fm_search and a.balance <= to_search:
					d = account_data_items(a, count)
					data.append(d)
					count += 1

	elif str(method) == 'date':
		fm_search = convert_search_to_date(search)
		to_search = convert_search_to_date(search2)

		for a in accounts:
			if str(user_id) == str(a.user_id):
				if a.date >= fm_search and a.date <= to_search:
					d = account_data_items(a, count)
					data.append(d)
					count += 1
	return data

def normal_account_search(accounts, search, user_id):
	data = []
	count = 0

	for a in accounts:
		if str(user_id) == str(a.user_id):
			m_type = get_account_type_text(a.isSavings)
			m_type = m_type.lower()

			if search_algorithm(search, a.account_number) == True:
				d = account_data_items(a, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, Decimal(a.balance)) == True:
				d = account_data_items(a, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, a.date) == True:
				d = account_data_items(a, count)
				data.append(d)
				count += 1
			elif search_algorithm(str(search).lower(), m_type) == True:
				d = account_data_items(a, count)
				data.append(d)
				count += 1
	return data

def advanced_loan_search(loans, search, search2, method, user_id):
	data = []
	count = 0

	if str(method) == 'money':
		fm_search = Decimal(str(search))
		to_search = Decimal(str(search2))

		for l in loans:
			if str(user_id) == str(l.user_id):
				if l.balance >= fm_search and l.balance <= to_search:
					d = getLoanListData(l, count)
					d['location'] = "Outstanding Balance"
					data.append(d)
					count += 1
				elif l.loan_amount >= fm_search and l.loan_amount <= to_search:
					d = getLoanListData(l, count)
					d['location'] = "Principal Balance"
					data.append(d)
					count += 1
				elif l.total_interest >= fm_search and l.total_interest <= to_search:
					d = getLoanListData(l, count)
					d['location'] = "Total Interest"
					data.append(d)
					count += 1
				elif l.payment >= fm_search and l.payment <= to_search:
					d = getLoanListData(l, count)
					d['location'] = "Monthly Payments"
					data.append(d)
					count += 1

	elif str(method) == 'date':
		fm_search = convert_search_to_date(search)
		to_search = convert_search_to_date(search2)

		for l in loans:
			if str(user_id) == str(l.user_id):
				if l.start_date >= fm_search and l.start_date <= to_search:
					d = getLoanListData(l, count)
					d['location'] = "Date of Loan"
					data.append(d)
					count += 1
				if l.end_date >= fm_search and l.end_date <= to_search:
					d = getLoanListData(l, count)
					d['location'] = "Final Payment Date(s)"
					data.append(d)
					count += 1
	return data

def normal_loan_search(loans, search, user_id):
	data = []
	count = 0

	for l in loans:
		if str(user_id) == str(l.user_id):
			m_type = int(l.loan_type)

			if m_type == 0:
				m_type = "personal"
			elif m_type == 1:
				m_type = "business"
			elif m_type == 2:
				m_type = "student"

			if search_algorithm(search, l.account_number) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, Decimal(l.balance)) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, Decimal(l.loan_amount)) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, Decimal(l.total_interest)) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, Decimal(l.payment)) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, Decimal(l.rate)) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, l.term) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, l.start_date) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(search, l.end_date) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
			elif search_algorithm(str(search).lower(), m_type) == True:
				d = getLoanListData(l, count)
				data.append(d)
				count += 1
	return data

def super_account_search(request):
	content = {}
	data = []
	a_list = []
	user_id = str(request.user.id)
	search = str(request.POST.get('search'))
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))
	search_type = str(request.POST.get('searchType'))
	method = ""
	search2 = ""
	m_sort = sort

	if direction == "descend":
		m_sort = "-" + sort

	accounts = Account.objects.all().order_by(m_sort)

	if search_type == 'normal':
		data = normal_account_search(accounts, search, user_id)
	elif search_type == 'advanced':
		method = str(request.POST.get('searchMethod'))
		search2 = str(request.POST.get('search2'))
		data = advanced_account_search(accounts, search, search2, method, user_id)

	content['status'] = 1

	if len(data) == 0:
		content['status'] = -1

	content['sort'] = sort
	content['direction'] = direction
	content['search'] = search
	content['search2'] = search2
	content['searchMethod'] = method
	content['searchType'] = search_type
	content['accounts'] = data
	content['isSearch'] = 1
	content['size'] = len(data)
	return content

def initiate_loan_search(request):
	content = {}
	data = []
	l_list = []
	user_id = str(request.user.id)
	search = str(request.POST.get('search'))
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))
	search_type = str(request.POST.get('searchType'))
	method = ""
	search2 = ""
	m_sort = sort

	if direction == "descend":
		m_sort = "-" + sort

	loans = Loan.objects.all().order_by(m_sort)

	if search_type == 'normal':
		data = normal_loan_search(loans, search, user_id)
	elif search_type == 'advanced':
		method = str(request.POST.get('searchMethod'))
		search2 = str(request.POST.get('search2'))
		data = advanced_loan_search(loans, search, search2, method, user_id)

	content['status'] = 1

	if len(data) == 0:
		content['status'] = -1

	content['sort'] = sort
	content['direction'] = direction
	content['search'] = search
	content['search2'] = search2
	content['searchMethod'] = method
	content['searchType'] = search_type
	content['loan'] = data
	content['isSearch'] = 1
	content['size'] = len(data)
	return content

def full_account(user, sort, direction):
	user_id = str(user.id)
	sorted_list = []
	count = 0

	if direction == "descend":
		sort = "-" + sort

	a_list = Account.objects.all().order_by(sort)

	for a in a_list:
		if str(a.user_id) == user_id:
			d = account_data_items(a, count)
			sorted_list.append(d)
			count += 1

	return sorted_list

def full_loan(user, sort, direction):
	user_id = str(user.id)
	sorted_list = []
	count = 0
	sort = str(sort)
	direction = str(direction)

	if direction == "descend":
		sort = "-" + sort

	l_list = Loan.objects.all().order_by(sort)

	for l in l_list:
		if str(l.user_id) == user_id:
			d = getLoanListData(l, count)
			sorted_list.append(d)
			count += 1

	return sorted_list

def getLoanListData(loan, index):
	d = {}

	if index % 2 == 0:
		d['class'] = 'lo_shade'
		d['class2'] = 'right_loan_balance'
	else:
		d['class'] = 'lo_clear'
		d['class2'] = 'right_loan_balance2'

	if index == 0:
		d['class'] = 'lo_select'
		d['class2'] = 'rl_selected'

	loan_type = int(loan.loan_type)

	if loan_type == 0:
		loan_type = "PERSONAL"
	elif loan_type == 1:
		loan_type = "BUSINESS"
	else:
		loan_type = "STUDENT"

	d['loan'] = loan
	d['balance'] = format_currency(loan.balance)
	d['principal'] = format_currency(loan.loan_amount)
	d['rate'] = str(float(loan.rate) * 100) + "%"
	d['total_interest'] = format_currency(loan.total_interest)
	d['payment'] = format_currency(loan.payment)
	d['term'] = str(loan.term) + " months"
	d['loan_type'] = loan_type
	d['index'] = index
	return d

def fetch_account_List(request):
	content = {}
	user = request.user
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))

	if sort == None or len(sort) == 0 or sort == "None" or sort == " " or sort == "null":
		sort = "date"
		direction = "descend"

	sorted_list = full_account(user, sort, direction)
	content['status'] = 1

	if len(sorted_list) == 0:
		content['status'] = -1

	content['isSearch'] = -1
	content['accounts'] = sorted_list
	content['sort'] = sort;
	content['direction'] = direction;
	content['size'] = len(sorted_list)
	return content

def fetch_loan_List(request):
	content = {}
	user = request.user
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))

	if sort == None or len(sort) == 0 or sort == "None" or sort == " " or sort == "null":
		sort = "balance"
		direction = "descend"

	sorted_list = full_loan(user, sort, direction)
	content['status'] = 1

	if len(sorted_list) == 0:
		content['status'] = -1

	content['isSearch'] = -1
	content['loan'] = sorted_list
	content['sort'] = sort;
	content['direction'] = direction;
	content['size'] = len(sorted_list)
	return content

def Withdrawal(request):
	content = {}
	withdraw = decoderCurrency(request, "dollars", "cents")
	acct_no = str(request.POST.get('account_number'))
	account = locate_account(acct_no)
	current_bal = Decimal(account.balance)
	d_type = request.POST.get('d_type')
	prev = account.balance

	new_bal = current_bal - withdraw
	account.balance = new_bal
	account.save()

	history = History(account_number=account.account_number)
	history.user_id = int(account.user_id)
	history.date = datetime.now().date()
	history.e_balance = new_bal
	history.b_balance = prev
	history.account_type = get_account_type_text(account.isSavings)
	history.description = "Withdrawal in the amount of $" + str(withdraw)
	history.action = get_action_from_index(1)
	history.save()

	content['history'] = history
	content['account'] = account
	content['previous'] = prev
	content['type'] = d_type
	return content

def Deposit(request):
	content = {}
	deposit = decoderCurrency(request, "dollars_w", "cents_w")
	acct_no = str(request.POST.get('account_number'))
	account = locate_account(acct_no)
	previous = account.balance
	m_type = request.POST.get('d_type')

	account.balance = deposit + Decimal(account.balance)
	account.save()

	history = History(account_number=account.account_number)
	history.user_id = int(account.user_id)
	history.account_type = get_account_type_text(account.isSavings)
	history.b_balance = previous
	history.e_balance = account.balance
	history.date = datetime.now().date()
	history.description = "Deposit in the amount of $" + str(deposit)
	history.action = get_action_from_index(2)
	history.save()

	content['account'] = account
	content['history'] = history
	content['type'] = m_type
	return content

def user_new_loan_only(request):
	content = {}
	decision = creditCheck()
	principal = decoderCurrency(request, "dollars", "cents")

	if decision['decision'] == True:
		content['url'] 		= "loans/user_new_loan_approved.html"
		rate 				= decision['interest']
		loan_type 			= int(request.POST.get('loan_type'))
		term 				= int(request.POST.get('term'))
		term 				= Decimal(term)
		monthly_payment		= calculatePayments(rate, term, principal)
		monthly_interest 	= monthly_payment - (principal/term)
		total_interest		= monthly_interest * term
		total 				= principal + total_interest

		content['rate'] 			= rate
		content['term'] 			= term
		content['monthly_payment'] 	= monthly_payment
		content['monthly_interest'] = monthly_interest
		content['total_interest'] 	= total_interest
		content['total_loan'] 		= total
		content['loan_type'] 		= loan_type

		if loan_type == 0:
			loan_tt = "Personal"
		elif loan_type == 1:
			loan_tt = "Business"
		else:
			loan_tt = "Student"

		content['loan_tt'] = loan_tt

		user_id = str(request.user.id)
		accounts = get_user_accounts(user_id)
		acct_nos = []

		for a in accounts:
			d = {}
			d['value'] = a.account_number
			d['option'] = get_account_type_text(a.isSavings) + " - " + str(a.account_number)
			acct_nos.append(d)

		if len(acct_nos) != 0:
			content['loan_message'] = "Where would you like to deposit the funds?"
			content['input_label'] = "Account:"
			content['acct_nos'] = json.dumps(acct_nos)
			content['action'] = 0
			content['button'] = "Deposit Funds"
		else:
			content['loan_message'] = "What type of account would you like to open?"
			content['input_label'] = "Type:"
			content['action'] = 1
			content['button'] = "Open Account"
			acct_nos.append('Checking')
			acct_nos.append('Savings')
			content['acct_nos'] = json.dumps(acct_nos)
	else:
		content['url'] = "loans/user_new_loan_denied.html"

	content['user'] = request.user
	content['format'] = format_currency(principal)
	content['principal'] = principal	
	return content

def user_new_loan_complete(request):
	content = {}
	date = datetime.now().date()
	user_id = str(request.user.id)
	principal = str(request.POST.get('principal'))
	rate = str(request.POST.get('rate'))
	term = str(request.POST.get('term'))
	monthly_payment = str(request.POST.get('monthly_payment'))
	monthly_interest = str(request.POST.get('monthly_interest'))
	total_interest = str(request.POST.get('total_interest'))
	total_loan = str(request.POST.get('total_loan'))
	loan_type = str(request.POST.get('loan_type'))
	action = str(request.POST.get('action'))
	account_number = None
	account_type = None
	loan_typef = None
	account = None

	principal = Decimal(format(float(principal), '.2f'))
	monthly_payment = Decimal(format(float(monthly_payment), '.2f'))
	monthly_interest = Decimal(format(float(monthly_interest), '.2f'))
	total_interest = Decimal(format(float(total_interest), '.2f'))
	total_loan = Decimal(format(float(total_loan), '.2f'))
	rate = Decimal(rate)
	term = int(term)
	end_date = date + relativedelta(months=+term)

	if loan_type == "0":
		loan_typef = "Personal"
	elif loan_type == "1":
		loan_typef = "Business"
	else:
		loan_typef = "Student"

	if action == "0":
		account_number = str(request.POST.get('deposit_account'))
		account = fetchAccount(account_number)
	elif action == "1":
		account_type = pythonBool(request.POST.get('account_type'))
		account = Account(user_id=user_id)
		account.account_number = fetchAccountNumber(8, False, True, "account")
		account.isSavings = account_type
		account.balance = principal
		account.date = date
		account.save()

	loan = Loan(user_id=user_id, account_number=account.account_number, loan_amount=principal)
	loan.balance = total_loan
	loan.loan_amount = principal
	loan.account_number = fetchAccountNumber(8, True, True, "loan")
	loan.term = term
	loan.rate = rate
	loan.payment = monthly_payment
	loan.total_interest = total_interest
	loan.loan_type = loan_type
	loan.start_date = date
	loan.end_date = end_date
	loan.save()

	history_acct = History(user_id=user_id, account_number=account.account_number, date=date, account_type=(get_account_type_text(account.isSavings)))
	history_loan = History(user_id=user_id, account_number=loan.account_number, date=date, account_type="Loan")

	history_acct.b_balance = 0.00
	history_acct.e_balance = principal
	history_acct.action = get_action_from_index(0)
	history_acct.description = "$" + format_currency(account.balance) + " deposited into new " + get_account_type_text(account.isSavings) 

	history_loan.b_balance = 0.00
	history_loan.e_balance = total_loan
	history_loan.action = get_action_from_index(5)
	history_loan.description = "Loan of " + format_currency(principal) + " deposited into " + get_account_type_text(account.isSavings) + ": " + str(account.account_number)

	history_acct.save()
	history_loan.save()

	content['sort'] = "start_date"
	content['direction'] = "descend"
	content['loan_typef'] = loan_typef
	content['principalf'] = "$" + format_currency(principal)
	content['ratef'] = str(rate * 100) + "%"
	content['monthly_interestf'] = "$" + format_currency(monthly_interest)
	content['total_interestf'] = "$" + format_currency(total_interest)
	content['termf'] = "$" + format_currency(monthly_payment) + " for " + str(term) + " months"
	content['totalf'] = "$" + format_currency(total_loan)
	return content

def fetchAccount(account_number):
	account = None
	a_list = Account.objects.all()

	for a in a_list:
		if str(account_number) == str(a.account_number):
			account = a
			break
	return account

def fetchDLoan(loan_id):
	loan = None
	l_list = Loan.objects.all()

	for l in l_list:
		if str(loan_id) == str(l.account_number):
			loan = l
			break
	return loan

def quick_grab_loan(request):
	loan_id = str(request.POST.get('account_number'))
	return fetchDLoan(loan_id)

def quick_rate(current_rate):
	current_rate = int(float(current_rate) * 100)
	rates = []
	random_index = random.randrange(0, 5)

	rates.append(format(Decimal(0.01), '.2f'))
	rates.append(format(Decimal(0.02), '.2f'))
	rates.append(format(Decimal(0.03), '.2f'))
	rates.append(format(Decimal(0.04), '.2f'))
	rates.append(format(Decimal(0.05), '.2f'))

	print "NEW RATE: " + str(rates[random_index])

	return rates[random_index]

def set_new_rate(loan, new_rate):
	data = {}

	prev_rate = int(float(loan.rate) * 100)
	prev_rate = str(prev_rate) + "%"
	data['rate'] = prev_rate
	data['principal'] = format_currency(loan.loan_amount)
	data['newRate'] = str(int(float(new_rate) * 100)) + "%" 
	return data

def init_refinance(request):
	content = {}
	loan = quick_grab_loan(request)
	rate = quick_rate(loan.rate)
	data = set_new_rate(loan, rate)
	new_loan = {}

	principal = Decimal(loan.loan_amount)
	term = Decimal(loan.term)
	monthly_payment	= calculatePayments(rate, term, principal)
	monthly_interest = monthly_payment - (principal/term)
	total_interest = monthly_interest * term
	total = principal + total_interest

	new_loan['rate'] = Decimal(rate)
	new_loan['payment'] = Decimal(monthly_payment)
	new_loan['total_interest'] = Decimal(total_interest)
	new_loan['balance'] = Decimal(total)

	content['rate'] = data['rate']
	content['monthly_payments'] = format_currency(format(monthly_payment, '.2f'))
	content['total_interest'] = format_currency(format(total_interest, '.2f'))
	content['loan_total'] = format_currency(format(total, '.2f'))
	content['principal'] = format_currency(loan.loan_amount)
	content['newRate'] = data['newRate']
	content['new_loan'] = new_loan
	content['new_rate'] = rate
	content['uf_payments'] = monthly_payment
	content['uf_interest'] = total_interest
	content['uf_total'] = total
	content['loan'] = loan
	return content

def refinance(request):
	content = {}
	account_number = request.POST.get('account_number')
	rate = request.POST.get('new_rate')
	monthly_payments = request.POST.get('monthly_payments')
	total_interest = request.POST.get('total_interest')
	loan_total = request.POST.get('loan_total')
	start_date = datetime.now().date()

	loan = fetchDLoan(str(account_number))
	b_balance = loan.balance
	loan.rate = Decimal(rate)
	loan.balance = format(Decimal(loan_total), '.2f')
	loan.payment = format(Decimal(monthly_payments), '.2f')
	loan.total_interest = format(Decimal(total_interest), '.2f')
	term = int(loan.term)
	end_date = start_date + relativedelta(months=+term)
	loan.end_date = end_date
	loan.save()

	rate = float(str(rate)) * 100
	rate = str(rate) + "%"

	history = History(user_id=loan.user_id, date=datetime.now().date(), account_number=loan.account_number)
	history.b_balance = b_balance
	history.e_balance = loan_total
	history.action = get_action_from_index(7)
	history.account_type = "Loan"
	history.description = "New loan rate of " + rate + " was applied to account"
	history.save()

	content['ratef'] = int(float(loan.rate) * 100)
	content['tif'] = format_currency(loan.total_interest)
	content['bf'] = format_currency(loan.balance)
	return content

def make_payment(request):
	content = {}
	loan_id = request.POST.get('account_number')
	payment = decoderCurrency(request, 'dollars', 'cents')
	loan = fetchDLoan(loan_id)
	curr_bal = loan.balance
	new_bal = curr_bal - payment
	loan.balance = new_bal
	loan.save()

	user_id = str(request.user.id)
	date = datetime.now().date()

	history = History(user_id=user_id, date=date, b_balance=curr_bal, e_balance=new_bal, account_number=loan_id)
	history.account_type = "Loan"
	history.action = get_action_from_index(6)
	history.description = "Payment received in the amount of $" +  str(format_currency(payment))
	history.save()
	content['payment'] = format_currency(payment)
	content['loan'] = loan
	content['balancef'] = format_currency(loan.balance)
	return content

def last4(account_number):
	account_number = str(account_number)
	last = account_number[4]
	last += account_number[5]
	last += account_number[6]
	last += account_number[7]
	return last

def get_user_accounts(user_id):
	all_accts = Account.objects.all()
	data = []

	for a in all_accts:
		if str(a.user_id) == str(user_id):
			data.append(a)
	return data

def grab_all_user_history(user_id, sort, direction):
	result = []
	sort = str(sort)
	user_id = str(user_id)
	direction = str(direction)

	if direction == 'descend':
		sort = "-" + sort

	history = History.objects.all().order_by(sort)

	for h in history:
		if user_id == str(h.user_id):
			result.append(h)
	return result

def get_h_acct(history):
	result = None
	proceed = True
	account = Account.objects.all().order_by('-account_number')
	loans = Loan.objects.all().order_by('-start_date')

	for a in account:
		if str(history.account_number) == str(a.account_number):
			return a
	for l in loans:
		if str(history.account_number) == str(l.account_number):
			return l
	return None

def propagateTransferOptions(request):
	options = {}
	fm_list = []
	to_list = []
	user_id = request.user.id
	account = get_user_accounts(user_id)

	selected_ds = request.POST.get('selected_dollars')
	selected_cs = request.POST.get('selected_cents')
	selected_fm = request.POST.get('selected_fm')
	selected_to = request.POST.get('selected_to')
	fm = request.POST.get('from_account')
	to = request.POST.get('to_account')

	if selected_ds == None:
		selected_ds = ""
	if selected_cs == None:
		selected_cs = ""
	if selected_fm == None:
		selected_fm = ""
	if selected_to == None:
		selected_to = ""
	if fm == None:
		fm = '0'
	if to == None:
		tm = '0'

	for a in account:
		if fm != str(a.account_number):
			to_list.append(a.account_number)
		else:
			selected_fm = a.account_number

		if to != str(a.account_number):
			fm_list.append(a.account_number)
		else:
			selected_to = a.account_number

	options['json_from'] = json.dumps(fm_list)
	options['json_to'] = json.dumps(to_list)
	options['fm_list'] = fm_list
	options['to_list'] = to_list
	options['selected_dollars'] = selected_ds
	options['selected_cents'] = selected_cs
	options['selected_from'] = selected_fm
	options['selected_to'] = selected_to
	return options 

def get_account_type_text(isSavings):
	m_type = "Checking"

	if str(isSavings) == 'True':
		m_type = "Savings"
	return m_type

def Transfer(request):
	content = {}
	transfer_amt = decoderCurrency(request, 't_dollars', 't_cents')
	fm_account_no = str(request.POST.get('from_account'))
	to_account_no = str(request.POST.get('to_account'))

	fm_account = locate_account(fm_account_no)
	to_account = locate_account(to_account_no)
	fm_prev_bn = fm_account.balance
	to_prev_bn = to_account.balance
	fm_type = get_account_type_text(fm_account.isSavings)
	to_type = get_account_type_text(to_account.isSavings)

	content['url'] = 'transfer.html'

	if fm_prev_bn < transfer_amt:
		content['status'] = 'transfer_error.html'
		content['type'] = fm_type
		content['balance'] = fm_prev_bn
		content['account'] = fm_account_no
		content['url'] = 'transfer_error.html'
	else:
		user_id = request.user.id
		date = datetime.now().date()
		to_balance = to_prev_bn + transfer_amt
		fm_balance = fm_prev_bn - transfer_amt

		to_account.balance = to_balance
		fm_account.balance = fm_balance

		to_account.save()
		fm_account.save()

		to_history = History(user_id=user_id)
		fm_history = History(user_id=user_id)

		to_history.b_balance = to_prev_bn
		fm_history.b_balance = fm_prev_bn

		to_history.e_balance = to_account.balance
		fm_history.e_balance = fm_account.balance

		to_history.account_number = to_account_no
		fm_history.account_number = fm_account_no

		to_history.date = date
		fm_history.date = date

		to_history.action = get_action_from_index(3)
		fm_history.action = get_action_from_index(9)

		to_history.account_type = get_account_type_text(fm_account.isSavings)
		fm_history.account_type = get_account_type_text(to_account.isSavings)

		to_history.description = "Transfer of $" + str(transfer_amt) + " received from " + fm_type + " account (" + fm_account_no + ")"
		fm_history.description = "Transfer of $" + str(transfer_amt) + " to " + to_type + " account (" + to_account_no + ")"

		to_history.save()
		fm_history.save()
		content['to_account'] = to_account
		content['fm_account'] = fm_account
		content['to_history'] = to_history
		content['fm_history'] = fm_history
	return content

def Delete_Account(request):
	content = {}
	account_number = str(request.POST.get('account_number'))
	account = locate_account(account_number)
	history = History.objects.all()

	for h in history:
		if account_number == str(h.account_number):
			h.delete()

	account.delete()
	content['account'] = account
	content['type'] = request.POST.get('d_type')
	content['status'] = 1
	return content

def New_Account_Active_User(request):
	content = {}
	user = request.user
	isSavings = pythonBool(request.POST.get('isSavings'))
	balance = decoderCurrency(request, 'dollars_w', 'cents_w')
	date = datetime.now().date()

	act_type_text = "Savings"
	if isSavings == False:
		act_type_text = "Checking"

	account = Account(user_id=int(user.id))
	account.date = date
	account.account_number = fetchAccountNumber(8, False, True, "account")
	account.isSavings = isSavings
	account.balance = balance
	account.save()

	history = History(user_id=int(user.id))
	history.account_number = account.account_number
	history.date = date
	history.account_type = get_account_type_text(account.isSavings)
	history.e_balance = Decimal(account.balance)
	history.b_balance = Decimal(0.00)
	history.description = "New " + act_type_text + " Account"
	history.action = get_action_from_index(0)
	history.save()

	content['account'] = account
	content['history'] = history
	content['type'] = act_type_text
	return content

def fetch_content(request, url):
	content = {}

	if url == "newAccount_0":
		content['title'] = "Lewis Bank | New Account"
		content['questions1'] = fetchSecurityQuestions1()
		content['questions2'] = fetchSecurityQuestions2()

	elif url == "newAccount_1":
		content = newUser_account(request)
		content['title'] = "Lewis Bank | New Account"

	elif url == "newLoan_0":
		content = newLoanDecision(request)

	elif url == "newLoan_1":
		content = buildLoan_init(request)

	elif url == "home":
		content = welcome_content(request)

	elif url == "summary":
		content = fetchAccountSummary(request)

	elif url == "accounts":
		content = fetchAccountContent(request)

	elif url == "loans":
		content = fetchLoansContent(request)

	elif url == "transactions":
		content = fetchTransactionsContent(request)

	elif url == "load_Thistory_list":
		content = load_Thistory_list(request)

	elif url == "load_history_search":
		content = mega_transaction_search(request)

	elif url == "profile":
		content = fetchProfileContent(request)

	elif url == "password":
		content = fetchPasswordContent(request)

	elif url == "loadNewPassword":
		content = loadNewPassword(request)

	elif url == "delete":
		content = fetchDeleteContent(request)

	elif url == "commitDelete":
		content = commitDelete(request)

	elif url == "sorted":
		content = fetch_sorted_content(request)

	elif url == "account_list":
		content = fetch_account_List(request)

	elif url == "withdraw":
		content = Withdrawal(request)

	elif url == "deposit":
		content = Deposit(request)

	elif url == "transfer":
		content = Transfer(request)

	elif url == "delete_account":
		content = Delete_Account(request)

	elif url == "add_account":
		content = New_Account_Active_User(request)

	elif url == "view_history":
		content = fetch_account_history(request)

	elif url == "trans0":
		content = propagateTransferOptions(request)

	elif url == "account_search":
		content = super_account_search(request)

	elif url == "user_new_loan":
		content = user_new_loan_only(request)

	elif url == "user_new_loan_complete":
		content = user_new_loan_complete(request)

	elif url == "refinance":
		content = refinance(request)

	elif url == "make_payment":
		content = make_payment(request)

	elif url == "load_refinance":
		content = init_refinance(request)

	elif url == "view_Payment_dates":
		content = fetch_payment_dates(request)

	elif url == "view_loan_history":
		content = fetch_loan_history(request)

	elif url == "loan_search":
		content = initiate_loan_search(request)

	elif url == "update_phone":
		content = update_user_phone(request)

	elif url == "loan_list":
		content = fetch_loan_List(request)

	return content

def fetch_date_ranges(user):
	dates 		= {}
	years 		= []
	months 		= []

	today 		= datetime.now().date()
	joined 		= user.date_joined.date()
	yy_joined 	= joined.year
	mm_joined 	= joined.month
	yy_now 		= today.year
	mm_now 		= today.month

	if yy_now == yy_joined:
		years.append(yy_now)
		no_months = abs(mm_now - mm_joined + 1)
		for i in range(no_months):
			d = {}
			d['value'] = mm_joined
			d['option'] = convert_month_toString(mm_joined)
			months.append(d)
			mm_joined += 1
	else:
		no_years = abs(yy_now - yy_joined + 1)
		for j in range(no_years):
			d = {}
			years.append(yy_joined)
			yy_joined += 1

		for k in range(12):
			d = {}
			d['value'] = k + 1
			d['option'] = convert_month_toString(k + 1)
			months.append(d)

	dates['day'] = joined.day 
	dates['years'] = json.dumps(years)
	dates['months'] = json.dumps(months)
	return dates

def commitDelete(request):
	content = {}
	user = request.user
	content['user'] = user
	user_id = str(user.id)

	history = History.objects.all()
	accounts = Account.objects.all()
	loans = Loan.objects.all()
	profile = getUserProfile(user)

	for h in history:
		if user_id == str(h.user_id):
			h.delete()

	for a in accounts:
		if user_id == str(a.user_id):
			a.delete()

	for l in loans:
		if user_id == str(l.user_id):
			l.delete

	profile.delete()
	user.delete()
	return content

def load_Thistory_list(request):
	content = {}
	user_id = str(request.user.id)
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))
	m_sort = sort
	h_list = []
	sorted_list = []
	count = 0

	if direction == 'descend':
		m_sort = "-" + sort

	history = History.objects.all().order_by(m_sort)

	for h in history:
		if user_id == str(h.user_id):
			h_list.append(h)

	for h in h_list:
		d = {}
		d['index'] = count

		if count % 2 == 0:
			d['class'] = 'history_clear'
		else:
			d['class'] = 'history_shade'

		d['b_balancef'] = format_currency(h.b_balance)
		d['e_balancef'] = format_currency(h.e_balance)
		d['history'] = h
		sorted_list.append(d)
		count += 1

	content['isSearch'] = -1
	content['size'] = count
	content['history'] = sorted_list
	content['sort'] = sort
	content['direction'] = direction
	return content

def update_user_phone(request):
	content = {}
	user = request.user
	phone1 = str(request.POST.get('ph1'))
	phone2 = str(request.POST.get('ph2'))
	phone3 = str(request.POST.get('ph3'))
	phone = "(" + phone1 + ") " + phone2 + "-" + phone3
	profile = getUserProfile(user)
	profile.phone = phone
	profile.save()
	content['phone'] = phone
	return content

def search_algorithm(search, value):
	match 		= False
	search 		= str(search)
	value 		= str(value)
	size 		= len(value)
	search_size = len(search)

	if search_size <= size:
		last_char 	= search_size - 1
		search 		= str(search)
		for i in range(size):
			t = ""
			if last_char != size:
				index = i
				for j in range(search_size):
					t += str(value[index])
					index += 1
				if t == search:
					match = True
					break
				else:
					last_char += 1
	return match

def convertPythonDate(date):
	result = None
	date = str(date)
	yy = ""
	mm = ""
	dd = ""
	temp = ""
	count = 0

	for d in date:
		if d == "-":
			if count == 0:
				mm = int(temp)
				temp = ""
				count += 1
			elif count == 1:
				dd = int(temp)
				temp = ""
		else:
			temp += d
	yy = int(temp)
	return datetime(yy, mm, dd).date()

def adv_lower(value):
	value = str(value)
	temp = ""

	for v in value:
		if v!="0" and v!="1" and v!="2" and v!="3" and v!="4" and v!="5" and v!="6" and v!="7" and v!="8" and v!="9":
			temp += v.lower()
		else:
			temp += v
	return temp


def fetch_loan_history(request):
	content = {}
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))
	loan_id = str(request.POST.get('account_number'))
	m_sort = sort
	h_list = []
	count = 0

	if direction == "descend":
		m_sort = "-" + sort

	history = History.objects.all().order_by(m_sort)

	for h in history:
		if loan_id == str(h.account_number):
			d = {}

			if count % 2 == 0:
				d['class'] = "hi_clear"
			else:
				d["class"] = "hi_shade"

			d['history'] = h
			d['starting_balance'] = format_currency(h.b_balance)
			d['ending_balance'] = format_currency(h.e_balance)
			count += 1
			h_list.append(d)

	content['account_number'] = loan_id
	content['sort'] = sort
	content['direction'] = direction
	content['history'] = h_list
	return content

def getLoanHIstory(loan_id, sort):
	history = History.objects.all().order_by(sort)
	loan_id = str(loan_id)
	data = []

	for h in history:
		if loan_id == str(h.account_number):
			data.append(h)
	return data

def fetch_payment_dates(request):
	content = {}
	dates = []
	init = {}
	loan_id = str(request.POST.get('account_number'))
	loan = fetchDLoan(loan_id)
	term = int(loan.term)
	m_type = int(loan.loan_type)

	if m_type == 0:
		m_type = "Personal"
	elif m_type == 1:
		m_type = "Business"
	else:
		m_type = "Student"

	dd = loan.start_date.day
	mm = loan.start_date.month
	yy = loan.start_date.year

	if dd > 5:
		mm += 1

	payment = datetime(yy, mm, 15).date()
	init['date'] = payment
	init['class'] = 'p_clear'
	dates.append(init)

	for i in range(term - 1):
		d = {}
		payment = payment + relativedelta(months=+1)
		d['date'] = payment

		if i % 2 == 0:
			d['class'] = 'p_shade'
		else:
			d['class'] = 'p_clear'
		dates.append(d)

	content['dates'] = dates
	content['m_type'] = m_type
	content['account_number'] = loan.account_number
	return content

def get_transaction_list_data(item, count):
	data = {}
	data['index'] = count

	if count % 2 == 0:
		data['class'] = 'history_clear'
	else:
		data['class'] = 'history_shade'

	data['b_balancef'] = format_currency(item.b_balance)
	data['e_balancef'] = format_currency(item.e_balance)
	data['history'] = item
	return data

def transaction_normal_search(transactions, search):
	results = []
	count = 0

	for t in transactions:
		if search_algorithm(search, t.account_number) == True:
			d = get_transaction_list_data(t, count)
			results.append(d)
			count += 1
		elif search_algorithm(search, t.b_balance) == True:
			d = get_transaction_list_data(t, count)
			results.append(d)
			count += 1
		elif search_algorithm(search, t.e_balance) == True:
			d = get_transaction_list_data(t, count)
			results.append(d)
			count += 1
		elif search_algorithm(search, t.date) == True:
			d = get_transaction_list_data(t, count)
			results.append(d)
			count += 1
		elif search_algorithm(search, t.account_type) == True:
			d = get_transaction_list_data(t, count)
			results.append(d)
			count += 1
		elif search_algorithm(search, t.action.action) == True:
			d = get_transaction_list_data(t, count)
			results.append(d)
			count += 1
	return results

def transaction_advanced_search(transactions, search, search2, method):
	results = []
	fm_search = None
	to_search = None
	method = str(method)
	count = 0

	if method == 'date':
		fm_search = convert_search_to_date(search)
		to_search = convert_search_to_date(search2)
		for t in transactions:
			if t.date >= fm_search and t.date <= to_search:
				d = get_transaction_list_data(t, count)
				results.append(d)
				count += 1
	elif method == 'money':
		fm_search = Decimal(search)
		to_search = Decimal(search2)
		for t in transactions:
			amount = abs(t.e_balance - t.b_balance)
			amount = Decimal(amount)
			if amount >= fm_search and amount <= to_search:
				d = get_transaction_list_data(t, count)
				results.append(d)
				count += 1
	return results

def mega_transaction_search(request):
	content = {}
	h_list = []
	sorted_list = []
	user_id = str(request.user.id)
	search_type = str(request.POST.get('searchType'))
	search = str(request.POST.get('search'))
	sort = str(request.POST.get('sort'))
	direction = str(request.POST.get('direction'))
	m_sort = sort
	method = ""
	search2 = ""

	if direction == "descend":
		m_sort = "-" + sort

	history = History.objects.all().order_by(m_sort)

	for h in history:
		if user_id == str(h.user_id):
			h_list.append(h)

	if search_type == "normal":
		sorted_list = transaction_normal_search(h_list, search)
	elif search_type == "advanced":
		search2 = str(request.POST.get('search2'))
		method = str(request.POST.get('searchMethod'))
		sorted_list = transaction_advanced_search(h_list, search, search2, method)

	content['isSearch'] = 1
	content['sort'] = sort
	content['search'] = search
	content['search2'] = search2
	content['searchType'] = search_type
	content['direction'] = direction
	content['method'] = method;
	content['user_id'] = user_id
	content['history'] = sorted_list
	content['size'] = len(sorted_list)
	return content

def convert_search_to_date(value):
	value = str(value)
	count = 0
	tp = ""
	yy = 0
	mm = 0
	dd = 0

	for v in value:
		if v == "-":
			if count == 0:
				mm = tp
				tp = ""
				count += 1
			elif count == 1:
				dd = tp
				tp = ""
				count += 1
		else:
			tp += v
	yy = int(tp)
	mm = int(mm)
	dd = int(dd)
	return datetime(yy, mm, dd).date()

def locate_user(request):
	content = {}
	user = None
	email = str(request.POST.get('email'))
	users = User.objects.all()

	for u in users:
		if email == str(u.email):
			user = u
			break

	if user == None:
		content['email'] = email
		content['url'] = "recover/error.html"
	else:
		content['url'] = "recover/pr1.html"
		profile = getUserProfile(user)
		q1_list = fetchSecurityQuestions1()
		q2_list = fetchSecurityQuestions2()

		q1 = q1_list[int(profile.question1)]['question']
		q2 = q2_list[int(profile.question2)]['question']

		content['q1'] = q1
		content['q2'] = q2

	content['user'] = user
	return content

def recovery_match(request):
	content = {}
	user_id = request.POST.get('user_id')
	user = User.objects.get(id=user_id)
	profile = getUserProfile(user)
	answer1 = str(request.POST.get('answer1'))
	answer2 = str(request.POST.get('answer2'))

	pa1 = str(profile.answer1)
	pa2 = str(profile.answer2)

	answer1 = answer1.lower()
	answer2 = answer2.lower()
	pa1 = pa1.lower()
	pa2 = pa2.lower()

	if answer1 == pa1 and answer2 == pa2:
		content['url'] = "recover/pr2.html"
		content['answer1'] = answer1
		content['answer2'] = answer2
	else:
		content['url'] = "recover/error2.html"
	content['user'] = user
	return content

def change_pw(request):
	content = {}
	user_id = request.POST.get('user_id')
	user = User.objects.get(id=user_id)
	password1 = str(request.POST.get('password1'))
	password2 = str(request.POST.get('password2'))

	if password1 == password2:
		user.set_password(password1)
		user.save()
		content['url'] = "recover/prSuccess.html"
	else:
		content['answer1'] = request.POST.get('answer1')
		content['answer2'] = request.POST.get('answer2')
		content['url'] = "recover/error3.html"
	content['user'] = user
	return content



		
		







		



	


















