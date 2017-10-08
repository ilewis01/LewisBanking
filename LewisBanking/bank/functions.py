from django.contrib.auth.models import User
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
		history.account_type = "Account"
		history.balance = account.balance
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
	history_account.account_type	= get_account_type_text(account.isSaving)
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
	user_id = str(user.id)
	profile = getUserProfile(user)
	name = name_abv(user)
	sort = request.POST.get('sort')
	direction = request.POST.get('direction')
	today = datetime.now()
	index = 0
	sorted_list = []
	user_loans = []
	m_sort = sort

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

	if direction == None or direction == "None" or direction == "null" or len(direction) == 0:
		direction = "descend"

	if sort == None or sort == "None" or sort == "null" or len(sort) == 0:
		sort = "start_date"

	sort = str(sort)
	direction = str(direction)

	if direction == "descend":
		m_sort = "-" + sort

	loans = Loan.objects.all().order_by(m_sort)

	for ln in loans:
		if str(ln.user_id) == user_id:
			user_loans.append(ln)

	for l in user_loans:
		d = {}

		loan_type = int(l.loan_type)
		if loan_type == 0:
			loan_type = "PERSONAL"
		elif loan_type == 1:
			loan_type = "BUSINESS"
		else:
			loan_type = "STUDENT"

		if dd > 15:
			mm += 1
		if mm == 1:
			yy += 1

		if index % 2 == 0:
			d['class'] = 'lo_shade'
			d['class2'] = 'right_loan_balance'
		else:
			d['class'] = 'lo_clear'
			d['class2'] = 'right_loan_balance2'

		if index == 0:
			d['class'] = 'lo_select'
			d['class2'] = 'rl_selected'

		payment_date = datetime(yy, mm, 15).date()

		d['account'] = l
		d['balance'] = format_currency(l.balance)
		d['principal'] = format_currency(l.loan_amount)
		d['rate'] = str(float(l.rate) * 100) + "%"
		d['total_interest'] = format_currency(l.total_interest)
		d['payment'] = format_currency(l.payment)
		d['term'] = str(l.term) + " months"
		d['loan_type'] = loan_type
		d['next_payment'] = payment_date

		item_id = "li" + str(index) + "_"
		d['index'] = index
		d['item_id'] = item_id
		d['account_no_id'] = item_id + "account_number"
		d['start_date_id'] = item_id + "start_date"
		d['loan_amount_id'] = item_id + "principal"
		d['balance_id'] = item_id + "balance"
		d['type_id'] = item_id + "type"
		d['rate_id'] = item_id + "rate"
		d['term_id'] = item_id + "term"
		sorted_list.append(d)
		index += 1

	content['size'] = index
	content['load_type'] = 0
	content['years'] = json.dumps(years)
	content['months'] = json.dumps(months)
	content['days_from'] = json.dumps(days_from)
	content['days_to'] = json.dumps(days_to)
	content['direction'] = direction
	content['sort'] = sort
	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['loans'] = sorted_list
	content['title'] = "Lewis Bank | Manage Loans"
	return content

def fetchTransactionsContent(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

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
	data = []
	acct_no = request.POST.get('selected_account')
	sort = request.POST.get('sort')
	direction = request.POST.get('direction')
	account = locate_account(acct_no)

	history = get_all_history(account, sort, direction)
	count = 0;
	m_type = get_account_type_text(account)

	for h in history:
		d = {}

		if count % 2 == 0:
			d['class'] = "hi_clear"
		else:
			d['class'] = "hi_shade"

		item_id = "hi" + str(count) + "_"

		d['item_id'] 		= item_id
		d['account_no_id'] 	= item_id + "account_number"
		d['date_id'] 		= item_id + "date"
		d['balance_id'] 	= item_id + "balance"
		d['type_id'] 		= item_id + "type"
		d['description_id'] = item_id + "action"
		d['action_id'] 		= item_id + "description"
		d['index'] 			= count
		d['history'] 		= h
		count += 1
		data.append(d)

	content['sort'] = sort
	content['direction'] = direction
	content['account_number'] = acct_no
	content['history'] = data;
	return content

def full_account(user, sort, direction):
	user_id = str(user.id)
	sorted_list = []
	count = 0
	class1 = "li_shade"
	class2 = "li_clear"

	if direction == "descend":
		sort = "-" + sort

	a_list = Account.objects.all().order_by(sort)

	for a in a_list:
		if str(a.user_id) == user_id:
			d = {}
			d['account'] = a
			d['history'] = get_all_history(a, 'date', 'descend')
			d['type'] = get_account_type_text(a.isSavings)

			if count % 2 == 0:
				d['class'] = class2
			else:
				d['class'] = class1

			item_id = 'li' + str(count) + "_"

			d['item_id'] = item_id
			d['account_no_id'] = item_id + "account_number"
			d['date_id'] = item_id + "date"
			d['balance_id'] = item_id + "balance"
			d['type_id'] = item_id + "type"
			d['index'] = count
			d['available'] = "Available Now:"
			d['format'] = format_currency(a.balance)
			count += 1

			sorted_list.append(d)

	return sorted_list

def mega_account_link_raw(h_list):
	data = []
	a_list = None
	count = 0
	class1 = "li_shade"
	class2 = "li_clear"

	for h in h_list:
		d = {}
		a_type = str(h.account_type)
		item_id = "li_" + str(count)
		d['history'] = h

		if count % 2 == 0:
			d['class'] = class2
		else:
			d['class'] = class1
		count += 1

		if a_type == "Account":
			a_list = Account.objects.all()
		elif a_type == "Loan":
			a_list = Loan.objects.all()

		for a in a_list:
			if str(a.account_number) == str(h.account_number):
				d['account'] = a
				break
		data.append(d)
	return data

def fetch_account_List(request):
	content = {}
	user = request.user
	sort = request.POST.get('sort')
	direction = None

	if sort == None:
		sort = "date"
		direction = "descend"
	else:
		sort = str(sort)
		direction = str(request.POST.get('direction'))

	opts = singleHistorySortOptions()
	options = json.dumps(opts)
	content['options'] = options

	sorted_list = full_account(user, sort, direction)
	content['options'] = options
	content['sorted_list'] = sorted_list
	content['sort'] = sort;
	content['direction'] = direction;
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
	history.account_type = "Account"
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
	history.account_type = "Account"
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

def init_refinance(request):
	content = {}
	loan_id = str(request.POST.get('account_number'))
	loan = fetchDLoan(loan_id)

	new_rate = newInterestRate()
	term = Decimal(loan.term)
	principal = Decimal(loan.loan_amount)
	monthly_payment = calculatePayments(new_rate, term, principal)
	monthly_payment = Decimal(format(float(monthly_payment), '.2f'))
	monthly_interest = Decimal(format(float(monthly_payment - (principal/term)), '.2f'))
	total_interest = Decimal(format(float(monthly_interest * term), '.2f'))
	total = principal + total_interest

	content['account_number'] = loan_id
	content['principal'] = format_currency(loan.loan_amount)
	content['rate'] = str(int(loan.rate * 100)) + "%"
	content['newRate'] = str(int(new_rate * 100)) + "%"
	content['new_rate'] = new_rate
	content['monthly_payments'] = format_currency(monthly_payment)
	content['total_interest'] = format_currency(total_interest)
	content['loan_total'] = format_currency(total)

	return content

def refinance(request):
	content = {}
	account_number = request.POST.get('account_number')
	rate = request.POST.get('new_rate')
	monthly_payments = request.POST.get('monthly_payments')
	total_interest = request.POST.get('total_interest')
	loan_total = request.POST.get('loan_total')
	start_date = datetime.now().date()

	monthly_payments = clear_format(monthly_payments)
	loan_total = clear_format(loan_total)

	loan = fetchDLoan(str(account_number))
	b_balance = Decimal(loan.balance)
	loan.rate = Decimal(rate)
	loan.balance = Decimal(loan_total)
	loan.payment = Decimal(monthly_payments)
	loan.total_interest = Decimal(total_interest)
	term = int(loan.term)
	end_date = start_date + relativedelta(months=+term)
	loan.end_date = end_date
	loan.save()

	rate = float(str(rate)) * 100
	rate = str(rate) + "%"

	history = History(user_id=loan.user_id, date=start_date, account_number=loan.account_number)
	history.b_balance = b_balance
	history.e_balance = loan_total
	history.action = get_action_from_index(7)
	history.account_type = "Loan"
	history.description = "New loan rate of " + rate + " was applied to account"
	history.save()

	content['loan'] = loan
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

def account_search_test(request):
	content = {}
	search = str(request.POST.get('search'))
	user_id = str(request.user.id)
	searchType = str(request.POST.get('searchType'))
	accounts = get_user_accounts(user_id)
	history = None
	match = False

	if searchType == "normal":
		for a1 in accounts:
			if search_algorithm(search, a1.account_number) == True:
				match = True

		if match == False:
			for a2 in accounts:
				if search_algorithm(search, str(a2.balance)) == True:
					match = True

		if match == False:
			for a4 in accounts:
				if search_algorithm(search, str(a4.date)) == True:
					match = True

		if match == False:
			for a5 in accounts:
				m_type = get_account_type_text(a5.isSavings)
				m_type = str(m_type).lower()
				search = search.lower()
				if search_algorithm(search, m_type) == True:
					match = True

		if match == False:
			for a in accounts:
				history = get_all_history(a, 'date', 'descend')

				if match == False:
					for h1 in history:
						if search_algorithm(search, str(h1.date)) == True:
							match = True

				if match == False:
					for h2 in history:
						if search_algorithm(search, str(h2.e_balance)) == True:
							match = True

				if match == False:
					for h3 in history:
						if search_algorithm(search, str(h3.e_balance)) == True:
							match = True

				if match == False:
					for h4 in history:
						if search_algorithm(search, str(h4.b_balance)) == True:
							match = True

				if match == False:
					for h5 in history:
						if search_algorithm(search.lower(), str(h5.action.action).lower()) == True:
							match = True

	elif searchType == "advanced":
		search2 = str(request.POST.get('search2'))
		advType = str(request.POST.get('advType'))
		content['search2'] = search2
		content['advType'] = advType
		history = None

		for a in accounts:
			m_fm = None
			m_to = None
			if advType == "date":
				history = get_all_history(a, 'date', 'descend')
				m_fm = convert_str_toDate(search)
				m_to = convert_str_toDate(search2)
				for h in history:
					if (h.date >= m_fm) and (h.date <= m_to):
						match = True
						break				
			elif advType == "money":
				history = grab_all_user_history(user_id, 'e_balance', 'descend')
				m_fm = str(search)
				m_to = str(search2)
				m_fm = Decimal(m_fm)
				m_to = Decimal(m_to)
				for h in history:
					transaction = abs(h.e_balance - h.b_balance)
					if (transaction >= m_fm) and (transaction <= m_to):
						match = True
						break
	content['search'] = search
	content['searchType'] = searchType
	content['match'] = match
	return content

def advanced_search(value, s_type, s_fm, s_to):
	match = False
	s_type = str(s_type)

	if s_type == "date":
		if value >= s_fm and value <= s_to:
			match = True 	
	return match

def super_account_search(request):
	content = {}
	searchType = str(request.POST.get('searchType'))
	if searchType == "normal":
		content = account_search_algorithm(request)
	elif searchType == "advanced":
		content = advanced_search_algorithm(request)
	return content

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

def advanced_search_algorithm(request):
	content = {}
	user_id = str(request.user.id)
	search = str(request.POST.get('search'))
	search2 = str(request.POST.get('search2'))
	user_id = str(request.user.id)
	advType = str(request.POST.get('advType'))
	matches = []
	count = 0
	m_fm = None
	m_to = None

	if advType == "date":
		m_fm = convert_str_toDate(search)
		m_to = convert_str_toDate(search2)
		content['adv_search_crit'] = str(m_fm) + " - " + str(m_to)
	
	if advType == "date":
		history = grab_all_user_history(user_id, 'date', 'descend')		
			
		for h in history:
			if (h.date >= m_fm) and (h.date <= m_to):
				account = get_h_acct(h)
				d = {}
				d['index'] = count
				d['account'] = h
				d['disp_account'] = str(h.account_number)
				d['disp_balance_b_head'] = "Starting Balance:"
				d['disp_balance_b_amt'] = "$" + format_currency(h.b_balance)
				d['disp_balance_e_head'] = "Ending Balance:"
				d['disp_balance_e_amt'] = "$" + format_currency(h.e_balance)
				d['m_type2'] = "Type: " + str(get_account_type_text(account))
				d['available'] = "Available Now:"
				d['format'] = format_currency(account.balance)
				d['description'] = str(h.action.action) + ": " + str(h.description)
				if count % 2 == 0:
					d['class'] = 'si_clear'
				else:
					d['class'] = 'si_shade'

				if str(h.account_type) == "Loan":
					d['m_type2'] = "Type: Loan"
					d['available'] = "Balance:"
				count += 1
				matches.append(d)				
	elif advType == "money":
		history = grab_all_user_history(user_id, 'e_balance', 'descend')
		m_fm = str(search)
		m_to = str(search2)
		content['adv_search_crit'] = str(m_fm) + " - " + str(m_to)
		m_fm = float(m_fm)
		m_to = float(m_to)
		for h in history:
			transaction = abs(h.e_balance - h.b_balance)
			if (transaction >= m_fm) and (transaction <= m_to):
				account = get_h_acct(h)
				d = {}
				d['index'] = count
				d['account'] = h
				d['disp_account'] = str(h.account_number)
				d['disp_balance_b_head'] = "Starting Balance:"
				d['disp_balance_b_amt'] = "$" + str(h.b_balance)
				d['disp_balance_e_head'] = "Ending Balance:"
				d['disp_balance_e_amt'] = "$" + str(h.e_balance)
				d['m_type2'] = "Type: " + str(get_account_type_text(account))
				d['format'] = format_currency(account.balance)
				d['description'] = str(h.action.action) + ": " + str(h.description)
				if count % 2 == 0:
					d['class'] = 'si_clear'
				else:
					d['class'] = 'si_shade'
				count += 1
				matches.append(d)
				
	content['matches'] = matches
	content['number'] = count
	content['phrase'] = "Results"
	if len(matches) == 1:
		content['phrase'] = "Result"
	return content

def account_search_algorithm(request):
	content = {}
	search = str(request.POST.get('search'))
	user_id = str(request.user.id)
	accounts = get_user_accounts(user_id)
	matches = []
	count = 0

	for a1 in accounts:
		if search_algorithm(search, a1.account_number) == True:
			d = {}
			d['index'] = count
			d['item_id'] = "s" + str(count) + "_"
			d['account'] = a1
			d['type'] = get_account_type_text(a1.isSavings) + ": " + str(a1.account_number)
			d['available'] = "Available Now:"
			d['m_type'] = get_account_type_text(a1.isSavings)
			d['format'] = format_currency(a1.balance)
			if count % 2 == 0:
				d['class'] = 'si_clear'
			else:
				d['class'] = 'si_shade'
			count += 1
			matches.append(d)

	for a2 in accounts:
		if search_algorithm(search, str(a2.balance)) == True:
			d = {}
			d['index'] = count
			d['item_id'] = "s" + str(count) + "_"
			d['account'] = a2
			d['type'] = get_account_type_text(a2.isSavings) + ": " + str(a2.account_number)
			d['available'] = "Available Now:"
			d['m_type'] = get_account_type_text(a2.isSavings)
			d['format'] = format_currency(a2.balance)
			if count % 2 == 0:
				d['class'] = 'si_clear'
			else:
				d['class'] = 'si_shade'
			count += 1
			matches.append(d)

	for a4 in accounts:
		if search_algorithm(search, str(a4.date)) == True:
			d = {}
			d['index'] = count
			d['item_id'] = "s" + str(count) + "_"
			d['account'] = a4
			d['available'] = "Available Now:"
			d['type'] = get_account_type_text(a4.isSavings) + ": " + str(a4.account_number)
			d['available'] = "Available Now:"
			d['m_type'] = get_account_type_text(a4.isSavings)
			d['format'] = format_currency(a4.balance)
			if count % 2 == 0:
				d['class'] = 'si_clear'
			else:
				d['class'] = 'si_shade'
			count += 1
			matches.append(d)

	for a5 in accounts:
		m_type = get_account_type_text(a5.isSavings)
		m_type = str(m_type).lower()
		search = search.lower()
		if search_algorithm(search, m_type) == True:
			d = {}
			d['index'] = count
			d['item_id'] = "s" + str(count) + "_"
			d['account'] = a4
			d['type'] = get_account_type_text(a5.isSavings) + ": " + str(a5.account_number)
			d['available'] = "Available Now:"
			d['m_type'] = get_account_type_text(a5.isSavings)
			d['format'] = format_currency(a5.balance)
			if count % 2 == 0:
				d['class'] = 'si_clear'
			else:
				d['class'] = 'si_shade'
			count += 1
			matches.append(d)

	for a in accounts:
		history = get_all_history(a, 'date', 'descend')
		ac_type = get_account_type_text(a.isSavings)

		for h1 in history:
			if search_algorithm(search, str(h1.date)) == True:
				d = {}
				d['index'] = count
				d['item_id'] = "s" + str(count) + "_"
				d['type'] = ac_type
				d['account'] = h1
				d['m_type'] = "Transaction: " + ac_type
				d['available'] = "Available Now:"
				d['text_account_no'] = "Account Number: " + str(h1.account_number)
				d['format'] = format_currency(h1.e_balance)
				d['description'] = str(h1.action.action) + ": " + str(h1.description)
				if count % 2 == 0:
					d['class'] = 'si_clear'
				else:
					d['class'] = 'si_shade'
				if str(h1.account_type) == "Loan":
					d['available'] = "Balance"
					d['m_type'] = "Loan"
				count += 1
				matches.append(d)

		for h2 in history:
			if search_algorithm(search, str(h2.e_balance)) == True:
				d = {}
				d['index'] = count
				d['item_id'] = "s" + str(count) + "_"
				d['type'] = ac_type
				d['account'] = h2
				d['m_type'] = "Transaction: " + ac_type
				d['available'] = "Available Now:"
				d['format'] = format_currency(h2.e_balance)
				d['description'] = str(h2.action.action) + ": " + str(h2.description)
				if count % 2 == 0:
					d['class'] = 'si_clear'
				else:
					d['class'] = 'si_shade'
				if str(h2.account_type) == "Loan":
					d['available'] = "Balance"
					d['m_type'] = "Loan"
				count += 1
				matches.append(d)

		for h3 in history:
			if search_algorithm(search, str(h3.b_balance)) == True:
				d = {}
				d['index'] = count
				d['item_id'] = "s" + str(count) + "_"
				d['type'] = ac_type
				d['account'] = h3
				d['m_type'] = "Transaction: " + ac_type
				d['available'] = "Available Now:"
				d['formatb'] = format_currency(h3.b_balance)
				d['description'] = str(h3.action.action) + ": " + str(h3.description)
				if count % 2 == 0:
					d['class'] = 'si_clear'
				else:
					d['class'] = 'si_shade'
				if str(h3.account_type) == "Loan":
					d['available'] = "Balance"
					d['m_type'] = "Loan"
				count += 1
				matches.append(d)

		for h4 in history:
			if search_algorithm(search, str(h4.account_number)) == True:
				d = {}
				d['index'] = count
				d['item_id'] = "s" + str(count) + "_"
				d['type'] = ac_type
				d['account'] = h4
				d['m_type'] = "Transaction: " + ac_type
				d['available'] = "Available Now:"
				d['format'] = format_currency(h4.e_balance)
				d['description'] = str(h4.action.action) + ": " + str(h4.description)
				if count % 2 == 0:
					d['class'] = 'si_clear'
				else:
					d['class'] = 'si_shade'
				if str(h4.account_type) == "Loan":
					d['available'] = "Balance"
					d['m_type'] = "Loan"
				count += 1
				matches.append(d)

		for h5 in history:
			if search_algorithm(search.lower(), str(h5.action.action).lower()) == True:
				d = {}
				d['index'] = count
				d['item_id'] = "s" + str(count) + "_"
				d['type'] = ac_type
				d['account'] = h5
				d['m_type'] = "Transaction: " + ac_type
				d['available'] = "Available Now:"
				d['format'] = format_currency(h5.e_balance)
				d['description'] = str(h5.action.action) + ": " + str(h5.description)
				if count % 2 == 0:
					d['class'] = 'si_shade'
				else:
					d['class'] = 'si_clear'
				if str(h5.account_type) == "Loan":
					d['available'] = "Balance"
					d['m_type'] = "Loan"
				count += 1
				matches.append(d)
	content['matches'] = matches
	content['number'] = count
	content['phrase'] = "Results"
	content['search'] = search
	if len(matches) == 1:
		content['phrase'] = "Result"
	return content

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

		to_history.account_type = 'Account'
		fm_history.account_type = 'Account'

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
	history.account_type = "Account"
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

	elif url == "profile":
		content = fetchProfileContent(request)

	elif url == "password":
		content = fetchPasswordContent(request)

	elif url == "delete":
		content = fetchDeleteContent(request)

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

	elif url == "account_search_test":
		content = account_search_test(request)

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

	return content

def search_algorithm(search, value):
	match 		= False
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

def initiate_loan_search(request):
	content = {}
	searchType = str(request.POST.get('searchType'))
	search = str(request.POST.get('search'))
	size = int(request.POST.get('size'))
	direction = str(request.POST.get('direction'))
	sort = str(request.POST.get('sort'))
	m_sort = sort
	user_id = str(request.user.id)
	loans = []
	results = []
	count = 0

	if direction == 'descend':
		m_sort = "-" + sort

	a_list = Loan.objects.all().order_by(m_sort)

	for a in a_list:
		if str(a.user_id) == user_id:
			loans.append(a)

	if searchType == "normal":
		for l in loans:
			t_search = int(l.loan_type)
			if t_search == 0:
				t_search = "personal"
			elif t_search == 1:
				t_search = 'business'
			else:
				t_search = "student"

			if search_algorithm(search, str(l.start_date)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(adv_lower(search), adv_lower(l.account_number)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.end_date)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.term)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.rate)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.balance)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.total_interest)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.loan_amount)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search, str(l.account_number)) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1
			elif search_algorithm(search.lower(), t_search) == True:
				d = getLoanListData(l, count)
				results.append(d)
				count += 1

	elif searchType == "advanced":
		search2 = str(request.POST.get('search2'))
		method = str(request.POST.get('searchMethod'))
		
		if method == 'date':
			fm_date = convertPythonDate(search)
			to_date = convertPythonDate(search2)
			for l2 in loans:
				if l2.start_date >= fm_date and l2.start_date <= to_date:
					d = getLoanListData(l2, count)
					results.append(d)
					count += 1
				elif l2.end_date >= fm_date and l2.end_date <= to_date:
					d = getLoanListData(l2, count)
					results.append(d)
					count += 1
		elif method == 'money':
			fm_amt = Decimal(search)
			to_amt = Decimal(search2)
			for l3 in loans:
				if Decimal(l3.payment) >= fm_amt and Decimal(l3.payment) <= to_amt:
					d = getLoanListData(l3, count)
					results.append(d)
					count += 1
				elif Decimal(l3.balance) >= fm_amt and Decimal(l3.balance) <= to_amt:
					d = getLoanListData(l3, count)
					results.append(d)
					count += 1
				elif Decimal(l3.loan_amount) >= fm_amt and Decimal(l3.loan_amount) <= to_amt:
					d = getLoanListData(l3, count)
					results.append(d)
					count += 1
				elif Decimal(l3.total_interest) >= fm_amt and Decimal(l3.total_interest) <= to_amt:
					d = getLoanListData(l3, count)
					results.append(d)
					count += 1

	content['load_type'] = 1

	if len(results) == 0 or count == 0:
		content['load_type'] = -1
		for zl in loans:
			d = getLoanListData(zl, count)
			results.append(d)
			count += 1

	content['size'] = count
	content['direction'] = direction
	content['sort'] = sort
	content['loans'] = results
	content['title'] = "Lewis Bank | Manage Loans"
	return content

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
		loan_type = "Personal"
	elif loan_type == 1:
		loan_type = "Business"
	else:
		loan_type = "Student"

	d['account'] = loan
	d['balance'] = format_currency(loan.balance)
	d['principal'] = format_currency(loan.loan_amount)
	d['rate'] = str(float(loan.rate) * 100) + "%"
	d['total_interest'] = format_currency(loan.total_interest)
	d['payment'] = format_currency(loan.payment)
	d['term'] = str(loan.term) + " months"
	d['loan_type'] = loan_type

	item_id = "li" + str(index) + "_"
	d['index'] = index
	d['item_id'] = item_id
	d['account_no_id'] = item_id + "account_number"
	d['start_date_id'] = item_id + "start_date"
	d['loan_amount_id'] = item_id + "principal"
	d['balance_id'] = item_id + "balance"
	d['type_id'] = item_id + "type"
	d['rate_id'] = item_id + "rate"
	d['term_id'] = item_id + "term"

	return d


def fetch_loan_history(request):
	content = {}
	history = []
	loan_id = str(request.POST.get("account_number"))
	sort = str(request.POST.get("sort"))
	direction = str(request.POST.get("direction"))
	m_sort = sort
	index = 0

	loan = fetchDLoan(loan_id)
	l_type = int(loan.loan_type)

	if l_type == 0:
		l_type = "Personal"
	elif l_type == 1:
		l_type = "Business"
	else:
		l_type = "Student"

	if direction == "descend":
		m_sort = "-" + sort

	h_list = getLoanHIstory(loan_id, m_sort)

	for h in h_list:
		d = {}
		d['index'] = index
		d['starting_balance'] = format_currency(h.b_balance)
		d['ending_balance'] = format_currency(h.e_balance)
		d['history'] = h

		if index % 2 == 0:
			d['class'] = "mhi_clear"
		else:
			d['class'] = "mhi_shade"
		history.append(d)
		index += 1

	content['sort'] = sort
	content['size'] = index
	content['direction'] = direction
	content['loan_type'] = l_type
	content['account_number'] = loan_id
	content['history'] = history
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




		
		







		



	


















