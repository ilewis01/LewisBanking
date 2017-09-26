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

def fetchSortedAccounts(user):
	accounts = {}
	du_list = []
	dd_list = []
	bu_list = []
	bd_list = []
	tu_list = []
	td_list = []
	au_list = []
	ad_list = []
	user_id = str(user.id)

	date_up = Account.objects.all().order_by('date')
	date_dn = Account.objects.all().order_by('-date')
	bal_up = Account.objects.all().order_by('balance')
	bal_dn = Account.objects.all().order_by('-balance')
	type_up = Account.objects.all().order_by('isSavings')
	type_dn = Account.objects.all().order_by('isSavings')
	account_up = Account.objects.all().order_by('account_number')
	account_dn = Account.objects.all().order_by('-account_number')


	for du in date_up:
		if str(du.user_id) == user_id:
			du_list.append(du)

	for dd in date_dn:
		if str(dd.user_id) == user_id:
			dd_list.append(dd)

	for bu in bal_up:
		if str(bu.user_id) == user_id:
			bu_list.append(bu)

	for bd in bal_dn:
		if str(bd.user_id) == user_id:
			bd_list.append(bd)

	for tu in type_up:
		if str(tu.user_id) == user_id:
			tu_list.append(tu)

	for td in type_dn:
		if str(td.user_id) == user_id:
			td_list.append(td)

	for au in account_up:
		if str(au.user_id) == user_id:
			au_list.append(au)

	for ad in account_dn:
		if str(ad.user_id) == user_id:
			ad_list.append(ad)


	accounts['date_up'] = link_history_to_account(du_list)
	accounts['date_down'] = link_history_to_account(dd_list)
	accounts['balance_up'] = link_history_to_account(bu_list)
	accounts['balance_down'] = link_history_to_account(bd_list)
	accounts['type_up'] = link_history_to_account(tu_list)
	accounts['type_down'] = link_history_to_account(td_list)
	accounts['account_number_up'] = link_history_to_account(au_list)
	accounts['account_number_down'] = link_history_to_account(ad_list)

	return accounts



def fetchSortedLoans(user):
	loans = {}
	user_id = str(user.id)

	bu_list = []
	bd_list = []
	pu_list = []
	pd_list = []
	ru_list = []
	rd_list = []
	du_list = []
	dd_list = []
	tyu_list = []
	tyd_list = []
	tmu_list = []
	tmd_list = []
	au_list = []
	ad_list = []

	balance_up = Loan.objects.all().order_by('balance')
	balance_dn = Loan.objects.all().order_by('-balance')

	principal_up = Loan.objects.all().order_by('loan_amount')
	principal_dn = Loan.objects.all().order_by('-loan_amount')

	type_up = Loan.objects.all().order_by('loan_type')
	type_dn = Loan.objects.all().order_by('-loan_type')

	term_up = Loan.objects.all().order_by('term')
	term_dn = Loan.objects.all().order_by('-term')

	rate_up = Loan.objects.all().order_by('rate')
	rate_dn = Loan.objects.all().order_by('-rate')

	date_up = Loan.objects.all().order_by('start_date')
	date_dn = Loan.objects.all().order_by('-start_date')

	account_up = Loan.objects.all().order_by('account_number')
	account_dn = Loan.objects.all().order_by('-account_number')

	for bu in balance_up:
		if str(bu.user_id) == user_id:
			bu_list.append(bu)

	for bd in balance_dn:
		if str(bd.user_id) == user_id:
			bd_list.append(bd)

	for pu in principal_up:
		if str(pu.user_id) == user_id:
			pu_list.append(pu)

	for pd in principal_dn:
		if str(pd.user_id) == user_id:
			pd_list.append(pd)

	for tyu in type_up:
		if str(tyu.user_id) == user_id:
			tyu_list.append(tyu)

	for tyd in type_dn:
		if str(tyd.user_id) == user_id:
			tyd_list.append(tyd)

	for tmu in term_up:
		if str(tmu.user_id) == user_id:
			tmu_list.append(tmu)

	for tmu in term_dn:
		if str(tmu.user_id) == user_id:
			tmu_list.append(tmu)

	for ru in rate_up:
		if str(ru.user_id) == user_id:
			ru_list.append(ru)

	for rd in rate_dn:
		if str(rd.user_id) == user_id:
			rd_list.append(rd)

	for du in date_up:
		if str(du.user_id) == user_id:
			du_list.append(du)

	for dd in date_dn:
		if str(dd.user_id) == user_id:
			dd_list.append(dd)

	for au in account_up:
		if str(au.user_id) == user_id:
			au_list.append(au)

	for ad in account_dn:
		if str(ad.user_id) == user_id:
			ad_list.append(ad)

	loans['balance_up'] = link_history_to_account(bu_list)
	loans['principal_up'] = link_history_to_account(pu_list)
	loans['type_up'] = link_history_to_account(tyu_list)
	loans['term_up'] = link_history_to_account(tmu_list)
	loans['rate_up'] = link_history_to_account(ru_list)
	loans['date_up'] = link_history_to_account(du_list)
	loans['balance_down'] = link_history_to_account(bd_list)
	loans['principal_down'] = link_history_to_account(pd_list)
	loans['type_down'] = link_history_to_account(tyd_list)
	loans['term_down'] = link_history_to_account(tmd_list)
	loans['rate_down'] = link_history_to_account(rd_list)
	loans['date_down'] = link_history_to_account(dd_list)
	loans['account_number_up'] = link_history_to_account(au_list)
	loans['account_number_down'] = link_history_to_account(ad_list)

	return loans

def fetchSortedHistory(user):
	history = {}
	du_list = []
	dd_list = []
	bu_list = []
	bd_list = []
	tu_list = []
	td_list = []
	au_list = []
	ad_list = []
	user_id = str(user.id)

	date_up = History.objects.all().order_by('date')
	date_dn = History.objects.all().order_by('-date')
	bal_up = History.objects.all().order_by('balance')
	bal_dn = History.objects.all().order_by('-balance')
	type_up = History.objects.all().order_by('account_type')
	type_dn = History.objects.all().order_by('-account_type')
	account_up = History.objects.all().order_by('account_number')
	account_dn = History.objects.all().order_by('-account_number')

	for du in date_up:
		if str(du.user_id) == user_id:
			du_list.append(du)

	for dd in date_dn:
		if str(dd.user_id) == user_id:
			dd_list.append(dd)

	for bu in bal_up:
		if str(bu.user_id) == user_id:
			bu_list.append(bu)

	for bd in bal_dn:
		if str(bd.user_id) == user_id:
			bd_list.append(bd)

	for tu in type_up:
		if str(tu.user_id) == user_id:
			tu_list.append(tu)

	for td in type_dn:
		if str(td.user_id) == user_id:
			td_list.append(td)

	for au in account_up:
		if str(au.user_id) == user_id:
			au_list.append(au)

	for ad in account_dn:
		if str(ad.user_id) == user_id:
			ad_list.append(ad)

	history['date_up'] = link_account_to_history(du_list)
	history['date_down'] = link_account_to_history(dd_list)
	history['balance_up'] = link_account_to_history(bu_list)
	history['balance_down'] = link_account_to_history(bd_list)
	history['type_up'] = link_account_to_history(tu_list)
	history['type_down'] = link_account_to_history(td_list)
	history['account_number_up'] = link_account_to_history(au_list)
	history['account_number_down'] = link_account_to_history(ad_list)

	return history

def link_history_to_account(account_list):
	c_list = []
	history_list = History.objects.all()

	for a in account_list:
		data = {}
		data['account'] = a

		for h in history_list:
			if str(a.account_number) == str(h.account_number):
				data['history'] = h
				break
		c_list.append(data)
	return c_list

def link_account_to_history(history_list):
	c_list = []
	account_list = Account.objects.all()
	loan_list = Loan.objects.all()

	for h in history_list:
		data = {}
		data['history'] = h
		data_type = str(h.account_type)
		m_list = None

		if data_type == "Account":
			m_list = account_list
		else:
			m_list = loan_list

		for m in m_list:
			if str(m.account_number) == str(h.account_number):
				data['account'] = m
				break
		c_list.append(data)
	return c_list


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

	elif url == "sorted":
		content = fetch_sorted_content(request)

	return content

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

def mega_account_link_raw(h_list):
	data = []
	a_list = None

	for h in h_list:
		d = {}
		d['history'] = h
		a_type = str(h.account_type)

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

def mega_sort(user, sort, direction, m_type):
	sorted_list = []

	if m_type == "Account" or m_type == "Loan":
		sorted_list = mega_account_sort(user, sort, direction, m_type)
	elif m_type == "History":
		sorted_list = mega_history_sort(user, sort, direction)

	return sorted_list


		



	


















