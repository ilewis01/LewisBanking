from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
	user 			= models.OneToOneField(User)
	is_superUser 	= models.BooleanField(default=False, blank=True)

	def __unicode__(self):
		return self.user.username
