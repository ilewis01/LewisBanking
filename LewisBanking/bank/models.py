from django.db import models
from django.contrib.auth.models import User

class Action(models.Model):
	index = models.IntegerField(default=0)
	action = models.CharField(max_length=50, default=0, blank=True, null=True)

	def __unicode__(self):
		return self.action


class profile(models.Model):
	user 			= models.OneToOneField(User)
	phone 			= models.CharField(max_length=16, default=0, blank=True, null=True)
	recoveryCode 	= models.CharField(max_length=30, default=None, blank=True, null=True)
	question1 		= models.IntegerField(default=0)
	question2 		= models.IntegerField(default=0)
	answer1 		= models.CharField(max_length=100, default=None, blank=True, null=True)
	answer2 		= models.CharField(max_length=100, default=None, blank=True, null=True)
	is_active	 	= models.BooleanField(default=False, blank=True)

	def __unicode__(self):
		return self.user.username

class Account(models.Model):
	user_id 		= models.IntegerField(default=0)
	account_number 	= models.CharField(max_length=8, default=None, blank=True, null=True)
	isSavings 		= models.BooleanField(default=False, blank=True)
	balance 		= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	date 	 		= models.DateField(default=None, blank=True, null=True)
	serializer 		= models.CharField(max_length=20, default="Account", blank=True, null=True)

	def __unicode__(self):
		return self.account_number

class Loan(models.Model):
	user_id 		= models.IntegerField(default=0)
	account_number 	= models.CharField(max_length=8, default=None, blank=True, null=True)
	loan_amount	 	= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	balance		 	= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	rate		 	= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	total_interest	= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	payment 		= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	loan_type 		= models.IntegerField(default=0)
	term 			= models.IntegerField(default=0)
	start_date 		= models.DateField(default=None, blank=True, null=True)
	end_date 		= models.DateField(default=None, blank=True, null=True)
	serializer 		= models.CharField(max_length=20, default="Loan", blank=True, null=True)

	def __unicode__(self):
		return str(self.account_number) + " - " + str(self.loan_amount)

class History(models.Model):
	user_id 		= models.IntegerField(default=0)
	account_number 	= models.CharField(max_length=8, default=None, blank=True, null=True)
	description 	= models.CharField(max_length=200, default=None, blank=True, null=True)
	b_balance		= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	e_balance		= models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
	date 			= models.DateField(default=None, blank=True, null=True)
	account_type 	= models.CharField(max_length=20, default=None, blank=True, null=True)
	action 			= models.ForeignKey(Action, default=None, blank=True, null=True)

	def __unicode__(self):
		return str(self.account_number)
