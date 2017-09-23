from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
	user 			= models.OneToOneField(User)
	accounts		= models.CharField(max_length=100000, default=0, blank=True, null=True)
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
	balance 		= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

	def __unicode__(self):
		return self.account_number

class Loan(models.Model):
	user_id 		= models.IntegerField(default=0)
	account_number 	= models.CharField(max_length=8, default=None, blank=True, null=True)
	loan_amount	 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	rate		 	= models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	loan_type 		= models.IntegerField(default=0)
	term 			= models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.account_number) + " - " + str(self.loan_amount)
