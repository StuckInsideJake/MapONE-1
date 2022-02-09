from django.test import TestCase

from mapone_api.user import UserClass
from mapone_api.models import User, Entry, Archive

from django.db.models import Max, F


# TODO - API tests too
# tests user class functions
class UserTestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		User.objects.all().delete()

		# class variables
		self.user_id = '1'
		# use own email
		self.email_address = ''
		self.password = 'password1!'
		self.archive_id_array = ''

		# create database object
		User.objects.create(
			user_id=self.user_id,
			email_address=self.email_address,
			password=self.password,
			archive_id_array=self.archive_id_array
		)

		# create class object
		self.user_class = UserClass()

	# test change password function
	def test_change_password(self):
		new_password = 'password2!'
		self.user_class.change_password(self.user_id, new_password)
		result = User.objects.filter(user_id=self.user_id).values('password')
		result = list(result)[0]['password']

		self.assertEqual(new_password, result)

	# test existing user
	def test_check_existing_user(self):
		result = self.user_class.check_existing_user(self.email_address)
		self.assertEqual(result, True)

		# use own test email
		test_email = ''
		result = self.user_class.check_existing_user(test_email)
		self.assertEqual(result, False)		

	# test create new user function
	def test_create_new_user(self):
		# use own test email
		test_email = ''
		test_password = 'password3!'
		self.user_class.create_new_user(test_email, test_password)
		result = User.objects.filter(email_address=test_email).values()
		result = list(result)[0]['email_address']

		self.assertEqual(result, test_email)

	# test delete user function
	def test_delete_user(self):
		self.user_class.delete_user(self.user_id)
		result = User.objects.filter(user_id=self.user_id)
		is_empty = []

		self.assertEqual(list(result), is_empty)

	# test generate user function
	def test_generate_user_id(self):
		test_id = self.user_class.generate_user_id() - 1
		result = User.objects.all().aggregate(Max('user_id'))
		result = result['user_id__max']

		self.assertEqual(test_id, result)

	# test verify email address, USE OWN TEST EMAILS
	# RUN TEST BY ITSELF --> ISSUES W API
	# def test_verify_email_address(self):
	# 	result = self.user_class.verify_email_address(self.email_address)
	# 	self.assertEqual(result, False)
		
	# 	test_email = 'abc'
	# 	result = self.user_class.verify_email_address(test_email)
	# 	self.assertEqual(result, False)

		# API doesn't allow multiple tests @ a time but test works
		#test_email = ''
		#result = self.user_class.verify_email_address(test_email)
		#self.assertEqual(result, True)

	# test verify password function
	def test_verify_password(self):
		test_password = 'testpassword1!'
		result = self.user_class.verify_password(test_password)
		self.assertEqual(result, True)

		test_password = 'abc'
		result = self.user_class.verify_password(test_password)
		self.assertEqual(result, False)
	
	# test verify user function
	def test_verify_user(self):
		result = self.user_class.verify_user(self.email_address, self.password)
		self.assertEqual(result, True)

		test_email = 'abc'
		result = self.user_class.verify_user(test_email, self.password)
		self.assertEqual(result, False)

		test_password = 'abc'
		result = self.user_class.verify_user(self.email_address, test_password)
		self.assertEqual(result, False)
