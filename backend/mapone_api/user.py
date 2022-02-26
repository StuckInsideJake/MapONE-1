from django.db.models import Max, F
from mapone_api.models import User
from django.core.mail import send_mail
from mapone.settings import DEFAULT_FROM_EMAIL
import requests

# user class
class UserClass:

	# change password
	def change_password(self, user_id, new_password):
		# verify password
		verified = self.verify_password(new_password)

		# if verified
		if verified:
			# look up user, change password
			User.objects.filter(user_id=user_id).update(
				password=new_password)

		# return operation success
		return verified

	# check if email address already exists
	def check_existing_user(self, email_address):
		# look up email address
		user_exists = User.objects.filter(email_address=email_address)

		# return if user exists
		return len(list(user_exists)) != 0

	# creates new user, returns user id
	def create_new_user(self, email_address, password):
		# check if email address is already used
		email_in_use = self.check_existing_user(email_address)

		# verify email address
		valid_email = self.verify_email_address(email_address)

		# verify password
		valid_password = self.verify_password(password)

		# if both verified
		if not email_in_use and valid_email and valid_password:
			# generate user id
			user_id = self.generate_user_id()

			# add to database
			User.objects.create(
				user_id=user_id,
				email_address=email_address,
				password=password
			)

			# return user_id
			return user_id

		return None

	# remove user account
	def delete_user(self, user_id):
		# look up user, remove user
		User.objects.get(user_id=user_id).delete()

		# update user ids in database
		User.objects.filter(user_id__gt=user_id).update(
			user_id=F('user_id') - 1)

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
	# django can do send_mass_mail()
	# need to figure out default from email address --> see settings.py
	def send_notification(self, user_id, subject, message):
		# gets user's email address
		email_address = User.objects.filter(
			user_id=user_id).values('email_address')
		
		# sends email to message
		send_mail(
			subject=subject,
			message=message,
			from_email=DEFAULT_FROM_EMAIL,
			recipient_list=[email_address]
		)

	# verifies new email address
	# uses external API
	def verify_email_address(self, email_address):
	# 	# check if email address is under another user
	# 	email_in_use = User.objects.filter(email_address=email_address).values('email_address')
	# 	email_in_use = len(list(email_in_use)) > 0

	# 	# if not found in database
	# 	if not email_in_use:
	# 		# send email API request
	# 		# uses https://www.abstractapi.com/
	# 		# need to change, plan only allows 100 API calls
	# 		# TODO - Ricardo find something different, research best option
	#		api_key = ''
	# 		response = requests.get(
	# 			f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email_address}"
	# 		)
	#
	# 		response = response.json()['is_smtp_valid']['value']
			
	# 		return response

	# 	return False
		# temp return value
		return True

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

			# return if password found
			return password_found

		return False
