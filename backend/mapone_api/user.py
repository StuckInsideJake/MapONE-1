from mapone_api.models import User, Entry, Archive
from django.core.mail import send_mail
import requests

# user class
class User:

	# constructor
	def __init__(self, email_address, password):
		self.user_id = generate_user_id()
		self.email_address = email_address
		self.password = password
		self.archive_id_array = ''

	# change password
	def change_password(user_id, new_password):
		# verify password
		verified = verify_password(new_password)

		# if verified
		if verified:
			# look up user, change password
			User.objects.get(user_id=user_id).update(
				password=new_password)

		# return operation success
		return verified

	# creates new user, returns user id
	def create_new_user(email_address, password):
		# verify email address
		valid_email = verify_email_address(email_address)

		# verify password
		valid_password = verify_password(password)

		# if both verified
		if valid_email and valid_password:
			# generate user id
			user_id = generate_user_id()

			# add to database
			User.objects.create(
				user_id=user_id,
				email_address=email_address,
				password=password
			)

			# return user_id
			return user_id

		# different type - issue?
		return False

	# remove user account
	def delete_user(user_id):
		# look up user, remove user
		User.objects.get(user_id=user_id).delete()

		# update user ids in database
		User.objects.filter(user_id__gt=user_id).update(
			user_id=F('user_id') - 1)

		# return none
		return None

	# creates new user id, returns user id
	def generate_user_id():
		# get largest user id in database
		user_id = User.objects.all().aggregate(Max('user_id'))

		# return last user id + 1
		return user_id['user_id'] + 1

	# sends email to inform user on automated search updates
	# django can do send_mass_mail()
	# need to figure out default from email address --> see settings.py
	def send_notification(user_id, subject, message):
		# gets user's email address
		email_address = User.objects.get(
			user_id=user_id).values('email_address')
		
		# sends email to message
		send_mail(
			subject=subject,
			message=message,
			from_email=DEFAULT_FROM_EMAIL,
			recipient_list=[email_address]
		)

		return None

	# verifies new email address
	# uses external API
	def verify_email_address(email_address):
		# set flag
		valid_email = False

		# check if email address is under another user
		email_in_use = User.objects.filter(email_address=email_address)

		# if not found in database
		if not email_in_use:
			# send email API request
			# uses https://www.abstractapi.com/ --> sign up and get own API key
			# need to change, plan only allows 100 API calls
			# TODO - Ricardo find something different, research best option
			# The following is the format
			response = requests.get(
				"https://emailvalidation.abstractapi.com/v1/?api_key=&email="
			)
			
			valid_email = response.content['is_smtp_valid']['value']

		return valid_email

	# verifies new password
	def verify_password(password):
		# get length
		length_requirment = 8
		length = len(password)
		special_chars = '~`!@#$%^&*()_-+=:;<,>.?/'

		# set flags
		letter = False
		digit = False
		special = False

		# check chars
		for char in password:
			# check for letter
			if char.isalpha():
				letter = True

			# check for numbers
			if char.isdigit():
				digit = True

			# check for special chars
			if char in special_chars:
				special = True

		# return flags
		return length >= length_requirment and letter and digit and special

	# checks if user is valid
	def verify_user(email_address, password):
		# checks database for email address
		password_found = User.objects.get(email_address=email_address).values(
			'password')

		# return if password found
		return password_found
