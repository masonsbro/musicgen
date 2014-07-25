import uuid
import hashlib

from django.db import models

# Create your models here.

class MusicGenUser(models.Model):

	email = models.EmailField(unique = True)
	passwordHash = models.CharField(max_length = 128)
	passwordSalt = models.CharField(max_length = 32)
	resetCode = models.CharField(max_length = 32, null = True, blank = True, default = "")

	def setPassword(self, password):
		# Generate random salt
		salt = uuid.uuid4().hex
		# Apply salt to password
		pSalted = password + salt
		# Hash the salted password
		pHashed = hashlib.sha512(pSalted).hexdigest()
		# Store the results for later
		self.passwordHash = pHashed
		self.passwordSalt = salt

	def checkPassword(self, password):
		# Apply salt to password
		pSalted = password + self.passwordSalt
		# Hash the salted password
		pHashed = hashlib.sha512(pSalted).hexdigest()
		# Check it against the stored one
		return self.passwordHash == pHashed

class Song:

	pass