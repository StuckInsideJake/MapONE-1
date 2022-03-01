from django.db.models import Max, F
from mapone_api.models import User
from mapone_api.constants import *
from django.core.mail import send_mail
from mapone.settings import DEFAULT_FROM_EMAIL
import requests
from email_validator import validate_email, EmailNotValidError

# user class
class UserClass:
	# need function to reset password
	# change password
	def change_password(self, user_id, new_password):
		# verify password
		verified = self.verify_password(new_password)

		# if verified
		if verified:
			# look up user, change password
			User.objects.filter(user_id=user_id).update(
				password=new_password)

			return SUCCESS

		# return operation success
		return INVALID_PASSWORD

	# check if email address already exists
	def check_existing_user(self, email_address):
		# look up email address
		user_exists = User.objects.filter(email_address=email_address).values()

		# return if user exists
		if user_exists:
			return list(user_exists)[0]['user_id']

		# no user
		return None

	# creates new user, returns user id
	def create_new_user(self, email_address, password):
		# check if email address is already used
		email_in_use = self.check_existing_user(email_address)

		# verify email address
		valid_email = self.verify_email_address(email_address)

		# verify password
		valid_password = self.verify_password(password)

		if not valid_email:
			return INVALID_EMAIL

		if not valid_password:
			return INVALID_PASSWORD

		# if verified
		if not email_in_use:
			# generate user id
			user_id = self.generate_user_id()

			# add to database
			User.objects.create(
				user_id=user_id,
				email_address=email_address,
				password=password
			)

			# return operation success
			return SUCCESS

		# user already exists
		return EMAIL_IN_USE

	# remove user account
	def delete_user(self, user_id):
		# look up user, remove user
		User.objects.get(user_id=user_id).delete()

		# update user ids in database
		User.objects.filter(user_id__gt=user_id).update(
			user_id=F('user_id') - 1)

		return SUCCESS

	# creates new user id, returns user id
	def generate_user_id(self):
		# get largest user id in database
		user_id = User.objects.all().aggregate(Max('user_id'))
		user_id = user_id['user_id__max']

		# if no user ids
		if(not user_id):
			# return first user value
			first_user = 1
			return first_user

		# return last user id + 1
		return user_id + 1

	# sends email to inform user on automated search updates
	def send_notification(self, user_id, subject, message):
		# gets user's email address
		email_address = User.objects.filter(
			user_id=user_id).values('email_address')
		email_address = list(email_address)[0]['email_address']
		
		# sends email to message
		send_mail(
			subject=subject,
			message=message,
			from_email=DEFAULT_FROM_EMAIL,
			recipient_list=[email_address]
		)

	# verifies new email address
	def verify_email_address(self, email_address):
		# check if email address is valid
		try:
			validate_email(email_address)
			return True

		# error
		except EmailNotValidError:
			return False

	# verifies new password
	def verify_password(self, password):
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
	def verify_user(self, email_address, password):
		# check existing user
		user_exists = self.check_existing_user(email_address)

		# if user exists
		if user_exists:
			# checks database for mtaching password
			password_found = User.objects.filter(email_address=email_address).values(
				'password')
			password_found = list(password_found)[0]['password'] == password

			# if password verified
			if password_found:
				# return login success
				return SUCCESS

			# else, incorrect password
			return INVALID_PASSWORD

		# user does not exist
		return INVALID_EMAIL
