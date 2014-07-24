from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.forms import ValidationError

from musicgenapp.models import *

import hashlib
import uuid

# Create your views here.

# This is the number of ratings each song should receive before moving to the next generation.
GENERATION_THRESHOLD = 3

# This is the highest generation that should be reached. After this generation, the song moves into archive mode and can no longer be rated. In archive mode, all iterations of the song are available for listening.
MAX_GENERATION = 10

# This is the lowest rating a song can have; below this it will automatically be deleted and a new song will be generated in its place.
LOWEST_RATING = 40

# This is the highest rating a song can have; above this it is automatically put in archive mode.
HIGHEST_RATING = 83

# These are the error messages to display when a form fails to submit.
ERROR_NO_EMAIL = "Please enter a valid email address."
ERROR_NO_PASSWORD = "Please enter a valid password."
ERROR_NO_PASSWORD_MATCH = "Please ensure the passwords match."
ERROR_BAD_LOGIN = "Email/password combination not found."

def index(req):
	return render(req, "index.html")

def about(req):
	return render(req, "about.html")

def list(req):
	return render(req, "list.html")

def signup(req):
	if req.method == 'POST':
		# POST, so get variables
		email = req.POST['email']
		password = req.POST['password']
		password_confirm = req.POST['password_confirm']
		errors = []
		# Validate email
		try:
			validate_email(email)
		except ValidationError:
			errors.append(ERROR_NO_EMAIL)
		# Validate password
		if not password:
			errors.append(ERROR_NO_PASSWORD)
		# Validate confirmation password
		if password != password_confirm:
			errors.append(ERROR_NO_PASSWORD_MATCH)
		# If there are errors, return the signup page with errors and prefilled email
		if errors:
			return render(req, "signup.html", {'errors': errors, 'email': email})
		else:
			# If there are no errors, create the user and redirect
			user = MusicGenUser(email = email, passwordHash = 'hash', passwordSalt = 'salt')
			user.setPassword(password)
			user.save()
			return redirect("/list/")
	else:
		# GET, so display form
		return render(req, "signup.html")

def login(req):
	if req.method == 'POST':
		# POST, so process login
		email = req.POST['email']
		password = req.POST['password']
		errors = []
		# Check if there is a user with that email address
		try:
			user = MusicGenUser.objects.get(email = email)
			# Compare passwords
			if not user.checkPassword(password):
				errors.append(ERROR_BAD_LOGIN)
		except:
			errors.append(ERROR_BAD_LOGIN)
		# If there are errors, return the login page with errors and prefilled email
		if errors:
			return render(req, "login.html", {'errors': errors, 'email': email})
		else:
			# If there are no errors, set the session variable and redirect
			req.session['email'] = email
			return redirect("/list/")
	else:
		# GET, so display form
		return render(req, "login.html")