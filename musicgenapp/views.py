from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.forms import ValidationError
from django.core.mail import send_mail
from django.core.files.storage import default_storage

from musicgenapp.models import *

import uuid

import sendgrid

# Create your views here.

# This is the base URL to link to in emails. EXCLUDE TRAILING SLASH.
BASE_URL = "http://musicgen.herokuapp.com"

# This is the subject line of the password reset email.
PW_RESET_SUBJECT = "MusicGen Password Reset"

# This is the HTML message body of the password reset email. Use %s for the link.
PW_RESET_BODY_HTML = """
Use the following link to reset your password.

%s

If you did not request this password reset, you can safely disregard this email.
"""

# This is the plaintext message body of the password reset email. Use %s for the link.
PW_RESET_BODY_TEXT = """
Use the following link to reset your password.

%s

If you did not request this password reset, you can safely disregard this email.
"""

# This is the email address from which password reset emails should be sent.
PW_RESET_FROM = "masonsbro@pearlandnerd.com"

# These are the login credentials for SendGrid (used to send password reset emails)
SG_USERNAME = "app27699523@heroku.com"
SG_PASSWORD = "4tnoo5h6"

# This is the number of ratings each song should receive before moving to the next generation.
GENERATION_THRESHOLD = 3

# This is the highest generation that should be reached. After this generation, the song moves into archive mode and can no longer be rated. In archive mode, all iterations of the song are available for listening.
MAX_GENERATION = 100

# This is the lowest rating a song can have; below this it is automatically put in archive mode.
LOWEST_RATING = 30

# This is the highest rating a song can have; above this it is automatically put in archive mode.
HIGHEST_RATING = 95

# These are the error messages to display when a form fails to submit.
ERROR_NO_EMAIL = "Please enter a valid email address."
ERROR_NO_PASSWORD = "Please enter a valid password."
ERROR_NO_PASSWORD_MATCH = "Please ensure the passwords match."
ERROR_BAD_LOGIN = "Email/password combination not found."
ERROR_CURRENT_PASSWORD = "That's not the correct current password."
ERROR_MISC = "Sorry, something went wrong!"
ERROR_SONG_NOT_FOUND = "Could not find a song with that ID."

# These are the success messages to display after a form has been submitted.
SUCCESS_PASSWORD_RESET = "If the email entered has a MusicGen account, it has been sent an email with instructions for resetting your password."
SUCCESS_ACCOUNT_CHANGED = "Account settings successfully changed!"

def check_logged_in(func):
	def wrapper(req, context = None, *args, **kwargs):
		# Having context as a parameter here allows for chaining of decorators later on
		if context is None:
			# Because can't have mutable default argument
			context = {}
		if 'email' in req.session:
			context['email'] = req.session['email']
			user = MusicGenUser.objects.get(email = req.session['email'])
			context['user'] = user
		return func(req, context, *args, **kwargs)
	return wrapper

def only_logged_in(func):
	def wrapper(req, *args, **kwargs):
		if 'email' in req.session:
			return func(req, *args, **kwargs)
		else:
			return redirect("/login/")
	return wrapper

def only_not_logged_in(func):
	def wrapper(req, *args, **kwargs):
		if 'email' not in req.session:
			return func(req, *args, **kwargs)
		else:
			return redirect("/list/")
	return wrapper

def only_admin(func):
	def wrapper(req, *args, **kwargs):
		if 'email' in req.session:
			user = MusicGenUser.objects.get(email = req.session['email'])
			if user.admin:
				return func(req, *args, **kwargs)
		return redirect("/list/")
	return wrapper

def init_alerts(func):
	def wrapper(req, context = None, *args, **kwargs):
		if context is None:
			context = {}
		if 'errors' not in context: context['errors'] = []
		if 'successes' not in context: context['successes'] = []
		if 'infos' not in context: context['infos'] = []
		return func(req, context, *args, **kwargs)
	return wrapper

@check_logged_in
def index(req, context):
	if 'email' not in req.session:
		return render(req, "index.html", context)
	else:
		return redirect("/list/")

@check_logged_in
def about(req, context):
	return render(req, "about.html", context)

@check_logged_in
def list(req, context):
	songs = Song.objects.filter(latest = True, wrapper__active = True).order_by('-pk')
	context['songs'] = []
	user = MusicGenUser.objects.get(email = req.session['email'])
	for song in songs:
		context['songs'].append((song, song.hasBeenRatedBy(user)))
	otherSongs = Song.objects.filter(latest = True, wrapper__active = False).order_by('-pk')
	context['songs'].extend(otherSongs)
	return render(req, "list.html", context)

@check_logged_in
@only_not_logged_in
@init_alerts
def forgot(req, context):
	if req.method == 'POST':
		# POST, so find user and reset password
		email = req.POST['email']
		try:
			# Invalid email should be treated differently than valid but nonexisting email
			try:
				validate_email(email)
			except ValidationError:
				context['errors'].append(ERROR_NO_EMAIL)
				# Return early to avoid catchall success message
				return render(req, "forgot.html", context)
			user = MusicGenUser.objects.get(email = email)
			resetCode = uuid.uuid4().hex
			user.resetCode = resetCode
			user.save()
			link = BASE_URL + "/reset/?code=" + resetCode
			subject = PW_RESET_SUBJECT
			messageHTML = PW_RESET_BODY_HTML % link
			messageText = PW_RESET_BODY_TEXT % link
			fromEmail = PW_RESET_FROM
			sg = sendgrid.SendGridClient(SG_USERNAME, SG_PASSWORD)
			mail = sendgrid.Mail(
				to = email,
				subject = subject,
				text = messageText,
				html = messageHTML,
				from_email = fromEmail)
			sg.send(mail)
		except Exception as e:
			# There was not a user with this email, but act like there was so that h4x0r5 can't brute force check if emails exist
			print e
		context['successes'].append(SUCCESS_PASSWORD_RESET)
	return render(req, "forgot.html", context)

@check_logged_in
@only_not_logged_in
@init_alerts
def reset(req, context):
	if req.method == 'POST':
		# The user has submitted the reset form.
		password = req.POST['password']
		password_confirm = req.POST['password_confirm']
		code = req.POST['resetCode']
		try:
			# The user has entered a new password
			if not password:
				context['errors'].append(ERROR_NO_PASSWORD)
			if password != password_confirm:
				context['errors'].append(ERROR_NO_PASSWORD_MATCH)
			if context['errors']:
				# Re-render with errors and keep the code as a hidden input field
				context['resetCode'] = code
				return render(req, "reset.html", context)
			user = MusicGenUser.objects.get(resetCode = code)
			user.resetCode = None
			user.setPassword(password)
			user.save()
			# Finally, log the user in
			req.session['email'] = user.email
			# Redirect to the list page and cry because this feature wasn't even really necessary in the first place I just thought it would be cool
			# Also, TODO: fix the camelCase/under_score variable names throughout the project
			return redirect("/list/")
		except Exception as e:
			# There wasn't a user found with that reset code
			print e
			context['errors'].append(ERROR_MISC)
			context['resetCode'] = code
			return render(req, "reset.html", context)
	else:
		# If the user didn't arrive here via a valid link with a reset code, send them to the login page
		if not 'code' in req.GET:
			return redirect("/login/")
		try:
			code = req.GET['code']
			user = MusicGenUser.objects.get(resetCode = code)
			# Save the reset code in the form so that once the user submits we can make sure it's the right account
			context['resetCode'] = code
			# The reset is actually legit, so display a password reset form
			return render(req, "reset.html", context)
		except:
			# If this wasn't a valid reset code, send user to login page
			return redirect("/login/")

@check_logged_in
@only_logged_in
def logout(req, context):
	del req.session['email']
	return redirect("/")

@check_logged_in
@only_logged_in
@init_alerts
def account(req, context):
	if req.method == 'POST':
		# The user has already made his changes
		password = req.POST['password']
		user = MusicGenUser.objects.get(email = req.session['email'])
		# Error if wrong current password
		if not user.checkPassword(password):
			context['errors'].append(ERROR_CURRENT_PASSWORD)
		new_password = req.POST['new_password']
		new_password_confirm = req.POST['new_password_confirm']
		if new_password != new_password_confirm:
			context['errors'].append(ERROR_NO_PASSWORD_MATCH)
		if context['errors']:
			return render(req, "account.html", context)
		# There were no errors, so make changes
		email = req.POST['email']
		if email:
			user.email = email
		if new_password:
			user.setPassword(new_password)
		user.save()
		context['successes'].append(SUCCESS_ACCOUNT_CHANGED)
	return render(req, "account.html", context)

@check_logged_in
@only_not_logged_in
@init_alerts
def signup(req, context):
	if req.method == 'POST':
		# POST, so get variables
		email = req.POST['email']
		context['email_prefill'] = email
		password = req.POST['password']
		password_confirm = req.POST['password_confirm']
		# Validate email
		try:
			validate_email(email)
		except ValidationError:
			errors.append(ERROR_NO_EMAIL)
		# Validate password
		if not password:
			context['errors'].append(ERROR_NO_PASSWORD)
		# Validate confirmation password
		if password != password_confirm:
			context['errors'].append(ERROR_NO_PASSWORD_MATCH)
		# If there are errors, return the signup page with errors and prefilled email
		if context['errors']:
			return render(req, "signup.html", context)
		else:
			# If there are no errors, create the user and redirect
			user = MusicGenUser(email = email, passwordHash = 'hash', passwordSalt = 'salt')
			user.setPassword(password)
			user.save()
			req.session['email'] = email
			return redirect("/list/")
	else:
		# GET, so display form
		return render(req, "signup.html")

@check_logged_in
@only_not_logged_in
@init_alerts
def login(req, context):
	if req.method == 'POST':
		# POST, so process login
		email = req.POST['email']
		context['email_prefill'] = email
		password = req.POST['password']
		# Check if there is a user with that email address
		try:
			user = MusicGenUser.objects.get(email = email)
			# Compare passwords
			if not user.checkPassword(password):
				context['errors'].append(ERROR_BAD_LOGIN)
		except:
			context['errors'].append(ERROR_BAD_LOGIN)
		# If there are errors, return the login page with errors and prefilled email
		if context['errors']:
			return render(req, "login.html", context)
		else:
			# If there are no errors, set the session variable and redirect
			req.session['email'] = email
			return redirect("/list/")
	else:
		# GET, so display form
		return render(req, "login.html")

@check_logged_in
@only_logged_in
@only_admin
def random(req, context):
	wrapper = SongWrapper()
	wrapper.save()
	song = Song.random(wrapper)
	song.save()
	song.generateFile()
	# idk if this is even necessary, but this method won't get called in production anyway so who cares
	song.save()
	wrapper.latest = song
	wrapper.save()
	return redirect("/admind/")

@check_logged_in
@only_logged_in
def rate(req, context):
	if req.method == 'POST':
		# This should only ever be POSTed
		value = int(req.POST['rating'])
		songID = int(req.POST['song'])
		try:
			song = Song.objects.get(pk = songID, latest = True, wrapper__active = True)
			try:
				prevRating = Rating.objects.get(song = song, user = MusicGenUser.objects.get(email = req.session['email']))
			except:
				prevRating = None
			if prevRating is not None or value > 100 or value < 0:
				# u best not be trynna vote twice
				raise
			song.addRating(value)
			rating = Rating(song = song, user = MusicGenUser.objects.get(email = req.session['email']), value = value)
			rating.save()
			if song.numRatings >= GENERATION_THRESHOLD:
				# Move to next generation
				if song.generation >= MAX_GENERATION or song.avgRating < LOWEST_RATING or song.avgRating > HIGHEST_RATING:
					# If one of the above conditions is met, we should archive it -- still display in list, but not able to be voted on
					song.archive()
				else:
					newSong = song.mutate()
					# TODO: try w/o this line?
					newSong.save()
					newSong.generateFile()
					# Or maybe without this one?
					newSong.save()
		except:
			pass
	return redirect("/list/")

@check_logged_in
@only_logged_in
def updateFiles(req, context):
	songs = Song.objects.all()
	for song in songs:
		song.generateFile()
	return redirect("/list/")

@check_logged_in
@only_logged_in
@only_admin
def admin(req, context):
	# TODO: limit 20 or so?
	context['songs'] = Song.objects.order_by('-pk')
	context['ratings'] = Rating.objects.order_by('-pk')[0:20]
	return render(req, "admin.html", context)

@check_logged_in
def song(req, context, id):
	song = Song.objects.get(pk = id)
	context['song'] = song
	context['history'] = Song.objects.filter(wrapper = song.wrapper).order_by('-pk')
	return render(req, "song.html", context)

@check_logged_in
@only_logged_in
@only_admin
def delete(req, context, id):
	song = Song.objects.get(pk = id)
	song.delete()
	return redirect("/admind/")

@check_logged_in
@only_logged_in
@only_admin
def mutate(req, context, id):
	song = Song.objects.get(pk = id)
	newSong = song.mutate()
	newSong.save()
	newSong.generateFile()
	newSong.save()
	return redirect("/admind/")