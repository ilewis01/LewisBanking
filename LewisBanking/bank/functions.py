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
	rate = float(rate)
	rate /= 100

	content['loan_type'] = loan_type

	principal = str(request.POST.get("principal"))
	interest = str(request.POST.get("interest"))
	payment = str(request.POST.get("payments"))
	principal = float(principal)
	interest = float(interest)
	payment = float(payment)
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
	loan.loan_amount 	= principal
	loan.balance 		= request.POST.get("total")
	loan.rate 			= rate
	loan.total_interest = interest
	loan.loan_type 		= enumerateLoanType(loan_type)
	loan.payment 		= payment
	loan.term 			= term
	loan.start_date 	= dates['start']
	loan.end_date 		= dates['end']
	loan.save()

	account = Account(user_id=user.id)
	account.account_number 	= fetchAccountNumber(8, False, True, "account")
	account.isSavings 		= pythonBool(request.POST.get("account_type"))
	account.balance 		= request.POST.get("principal")
	account.date 			= dates['start']
	account.save()

	encode = str(account.id) + "~" + str(loan.id) + "~"
	pfile.accounts = encode
	pfile.save()

	history_account 				= History()
	history_account.date 			= dates['start']
	history_account.account_type	= "Account"
	history_account.user_id			= user.id
	history_account.description 	= "Account Opened"
	history_account.account_number	= account.account_number
	history_account.balance 		= account.balance
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
	history_loan.balance 			= loan.balance
	listory_loan.action 			= get_action_from_index(5)
	history_loan.save()

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
			term 				= float(term)
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
			content['principal']	= principal
			content['payments'] 	= monthly_payment
			content['interest']		= total_interest
			content['total']		= total

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
	sort = request.POST.get('sort')
	sorted_list = None
	direction = None
	m_type = "History"

	if sort == None:
		sort = "date"
		direction = "descend"
	else:
		direction = str(request.POST.get("direction"))

	sorted_list = mega_sort(user, sort, direction, m_type)

	content['name'] = name
	content['user'] = user
	content['sorted_list'] = sorted_list
	content['title'] = "Lewis Bank | Summary"
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
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

	content['name'] = name
	content['user'] = user
	content['profile'] = profile
	content['title'] = "Lewis Bank | Manage Accounts"
	return content

def fetchLoansContent(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

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
	class1 = "li_clear"
	class2 = "li_shade"

	if direction == "descend":
		sort = "-" + sort

	a_list = Account.objects.all().order_by(sort)

	for a in a_list:
		if str(a.user_id) == user_id:
			d = {}
			d['account'] = a
			d['history'] = get_all_history(a, 'date', 'descend')
			d['type'] = 'Savings'

			if a.isSavings == False:
				d['type'] = 'Checking'

			if count % 2 == 0:
				d['class'] = class1
			else:
				d['class'] = class2

			item_id = 'li' + str(count) + "_"

			d['item_id'] = item_id
			d['account_no_id'] = item_id + "account_number"
			d['date_id'] = item_id + "date"
			d['balance_id'] = item_id + "balance"
			d['type_id'] = item_id + "type"
			d['index'] = count
			count += 1

			sorted_list.append(d)

	return sorted_list

def mega_account_link_raw(h_list):
	data = []
	a_list = None
	count = 0
	class1 = "li_clear"
	class2 = "li_shade"

	for h in h_list:
		d = {}
		a_type = str(h.account_type)
		item_id = "li_" + str(count)
		d['history'] = h

		if count % 2 == 0:
			d['class'] = class1
		else:
			d['class'] = class2
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

def propagateTransferOptions(request):
	options = {}
	fm_list = []
	to_list = []
	user_id = request.user.id
	account = get_user_accounts(user_id)
	li_info = []
	index_to = 1
	index_fm = 1

	selected_to = request.POST.get('selected_to')
	selected_fm = request.POST.get('selected_fm')
	fm = request.POST.get('from_account')
	to = request.POST.get('to_account')

	if selected_to == None:
		selected_to = 0
	if selected_fm == None:
		selected_fm = 0

	if fm == None:
		fm = '0'
	if to == None:
		tm = '0'

	for a in account:
		if fm != str(a.account_number):
			to_list.append(a.account_number)
			index_fm += 1
		else:
			selected_fm = a.account_number

		if to != str(a.account_number):
			fm_list.append(a.account_number)
			index_to += 1
		else:
			selected_to = a.account_number

	options['fm_list'] = fm_list
	options['to_list'] = to_list
	options['from_index'] = selected_fm
	options['to_index'] = selected_to
	return options 

def get_account_type_text(isSavings):
	m_type = "Checking"

	if isSavings == True:
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

		to_history.action = get_action_from_index(9)
		fm_history.action = get_action_from_index(3)

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

	return content


		
		







		



	


















