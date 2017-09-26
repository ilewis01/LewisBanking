from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import random
import json
import json as simplejson

from bank.models import profile, Account, Loan, History


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
		history.balance = account.balance
		history.date = datetime.now().date()
		history.description = "Account Opened"

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
	history_account.description 	= "Account Opened"
	history_account.account_number	= account.account_number
	history_account.balance 		= account.balance
	history_account.save()

	a_type = "Checking"

	if account.isSavings == True:
		a_type = "Savings"

	history_loan 	 				= History()
	history_loan.date 				= dates['start']
	history_loan.description 		= "Loan Approved and deposited into " + a_type + ": " + str(account.account_number)
	history_loan.account_number		= loan.account_number
	history_loan.balance 			= loan.balance
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
	content['title'] = "Welcome to Lewis Bank"
	return content

def fetchAccountSummary(request):
	content = {}
	user = request.user
	profile = getUserProfile(user)
	name = name_abv(user)

	content['name'] = name
	content['user'] = user
	content['profile'] = profile
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
	dollars = float(dollars)
	cents = "0." + str(request.POST.get(cents_id))
	cents = float(cents)
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

	return content

	


















