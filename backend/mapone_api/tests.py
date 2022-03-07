from django.test import TestCase

from mapone_api.user import UserClass
from mapone_api.entry import EntryClass
from mapone_api.archive import ArchiveClass

from mapone_api.models import User, Entry, Archive
from mapone_api.constants import *

from django.db.models import Max

from rest_framework import status
from rest_framework.test import APIClient

import datetime


# tests user, entry, and archive APIs
class APITestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		User.objects.all().delete()
		Entry.objects.all().delete()
		Archive.objects.all().delete()

		# define variables
		self.client = APIClient()
		self.user_url = '/user/'
		self.entry_url = '/entry/'
		self.archive_url = '/archive/'
		# use own test email
		self.email_address = ''
		self.password = 'password1?'

	def test_no_params(self):
		response = self.client.get(self.user_url)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.get(self.entry_url)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.get(self.archive_url)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		params = {'action': CREATE_USER}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_wrong_action(self):
		params = {
			'action': 100,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, None)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.get(self.entry_url, params)
		self.assertEqual(response.data, None)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.data, INVALID_EMAIL)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		User.objects.create(
			user_id=1,
			email_address=self.email_address,
			password=self.password
		)
		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.data, None)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_user_action(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_login(self):
		User.objects.all().delete()
		params = {
			'action': LOGIN,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, INVALID_EMAIL)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, SUCCESS)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		params = {
			'action': LOGIN,
			'email_address': self.email_address,
			'password': 'test_password'
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, INVALID_PASSWORD)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_change_password_action(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)

		params = {
			'action': CHANGE_PASSWORD,
			'email_address': self.email_address,
			'password': self.password,
			'new_password': 'password2?'
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, SUCCESS)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_user_action(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)

		params = {
			'action': DELETE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, SUCCESS)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		response = self.client.get(self.user_url, params)
		self.assertEqual(response.data, INVALID_EMAIL)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_main_page_action(self):
		Entry.objects.create(
			entry_id=1,
			source_name='test',
			source_link='test',
			article_title='test',
			publication_date=datetime.date(2000, 1, 1),
			author_list='test',
			map_body='test',
			map_scale='test'
		)
		params = {'action': MAIN_PAGE}
		response = self.client.get(self.entry_url, params)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_search_keyword_action(self):
		Entry.objects.create(
			entry_id=1,
			source_name='test',
			source_link='test',
			article_title='test',
			publication_date=datetime.date(2000, 1, 1),
			author_list='test',
			map_body='test',
			map_scale='test'
		)
		params = {'action': SEARCH_KEYWORD, 'keyword': 'test'}
		response = self.client.get(self.entry_url, params)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		params = {'action': SEARCH_KEYWORD, 'keyword': 'abc'}
		response = self.client.get(self.entry_url, params)
		self.assertEqual(response.data, None)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_filter_year_action(self):
		Entry.objects.create(
			entry_id=1,
			source_name='test',
			source_link='test',
			article_title='test',
			publication_date=datetime.date(2000, 1, 1),
			author_list='test',
			map_body='test',
			map_scale='test'
		)
		params = {'action': FILTER_YEAR, 'first_year': '2000', 'second_year': '2002'}
		response = self.client.get(self.entry_url, params)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_archive_action(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)

		params = {
			'action': CREATE_ARCHIVE,
			'email_address': self.email_address,
			'password': self.password,
			'keyword': 'test',
			'frequency': 'test'
		}
		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.data, SUCCESS)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_display_user_archives(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)

		params = {
			'action': CREATE_ARCHIVE,
			'email_address': self.email_address,
			'password': self.password,
			'keyword': 'test',
			'frequency': 'test'
		}
		response = self.client.get(self.archive_url, params)

		params = {
			'action': DISPLAY_USER_ARCHIVES,
			'email_address': self.email_address,
			'password': self.password,
		}
		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_archive_action(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)

		params = {
			'action': CREATE_ARCHIVE,
			'email_address': self.email_address,
			'password': self.password,
			'keyword': 'test',
			'frequency': 'test'
		}
		response = self.client.get(self.archive_url, params)

		params = {
			'action': DELETE_ARCHIVE,
			'email_address': self.email_address,
			'password': self.password,
		}

		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.data, None)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		params = {
			'action': DELETE_ARCHIVE,
			'email_address': self.email_address,
			'password': self.password,
			'keyword': 'test'
		}
		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.data, SUCCESS)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_frequency_action(self):
		params = {
			'action': CREATE_USER,
			'email_address': self.email_address,
			'password': self.password
		}
		response = self.client.get(self.user_url, params)

		params = {
			'action': CREATE_ARCHIVE,
			'email_address': self.email_address,
			'password': self.password,
			'keyword': 'test',
			'frequency': 'week'
		}
		response = self.client.get(self.archive_url, params)

		params = {
			'action': UPDATE_FREQUENCY,
			'email_address': self.email_address,
			'password': self.password,
			'keyword': 'test',
			'new_frequency': 'month'
		}
		response = self.client.get(self.archive_url, params)
		self.assertEqual(response.data, SUCCESS)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

# tests user class functions
class UserTestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		User.objects.all().delete()

		# class variables
		self.user_id = 1
		# use own test email
		self.email_address = ''
		self.password = 'password1!'

		# create database object
		User.objects.create(
			user_id=self.user_id,
			email_address=self.email_address,
			password=self.password
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

	# test existing user function
	def test_check_existing_user(self):
		result = self.user_class.check_existing_user(self.email_address)
		self.assertEqual(result, self.user_id)

		# use own test email
		test_email = ''
		result = self.user_class.check_existing_user(test_email)
		self.assertEqual(result, None)		

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

	# test generate user id function
	def test_generate_user_id(self):
		test_id = self.user_class.generate_user_id() - 1
		result = User.objects.all().aggregate(Max('user_id'))
		result = result['user_id__max']

		self.assertEqual(test_id, result)

		User.objects.all().delete()
		test_id = self.user_class.generate_user_id()
		result = 1

		self.assertEqual(test_id, result)

	# test send notification
	def test_send_notification(self):
		# dummy test, check email
		subject = 'test'
		message = 'test'
		self.user_class.send_notification(self.user_id, subject, message)

	# test verify email address
	def test_verify_email_address(self):
		result = self.user_class.verify_email_address(self.email_address)
		self.assertEqual(result, True)
		
		test_email = 'abc'
		result = self.user_class.verify_email_address(test_email)
		self.assertEqual(result, False)

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
		self.assertEqual(result, SUCCESS)

		test_email = 'abc'
		result = self.user_class.verify_user(test_email, self.password)
		self.assertEqual(result, INVALID_EMAIL)

		test_password = 'abc'
		result = self.user_class.verify_user(self.email_address, test_password)
		self.assertEqual(result, INVALID_PASSWORD)

# tests entry class functions
class EntryTestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		Entry.objects.all().delete()

		# class variables
		self.entry_id = 1
		self.source_name = 'test'
		self.source_link = 'test'
		self.article_title = 'test'
		self.publication_date = datetime.date(2000, 1, 1)
		self.author_list = 'test'
		self.map_body = 'test'
		self.map_scale = None

		# create database object
		Entry.objects.create(
			entry_id=self.entry_id,
			source_name=self.source_name,
			source_link=self.source_link,
			article_title=self.article_title,
			publication_date=self.publication_date,
			author_list=self.author_list,
			map_body=self.map_body,
			map_scale=self.map_scale
		)

		# create class object
		self.entry_class = EntryClass()

	# test existing entry function
	def test_check_existing_entry(self):
		result = self.entry_class.check_existing_entry(
			self.article_title, 
			self.author_list
		)
		self.assertEqual(result, True)

		test_input = 'abc'
		result = self.entry_class.check_existing_entry(
			test_input,
			test_input
		)
		self.assertEqual(result, False)

	# test create new entry function
	def test_create_new_entry(self):
		Entry.objects.all().delete()
		result = self.entry_class.create_new_entry(
			self.source_name,
			self.source_link,
			self.article_title,
			self.publication_date,
			self.author_list,
			self.map_body,
			self.map_scale
		)

		entry_id = Entry.objects.filter(
			article_title=self.source_name,
			author_list=self.author_list
		).values('entry_id')
		entry_id = list(entry_id)[0]['entry_id']

		self.assertEqual(result, entry_id)

	# test delete entry function
	def test_delete_entry(self):
		self.entry_class.delete_entry(self.entry_id)
		result = Entry.objects.filter(entry_id=self.entry_id)
		is_empty = []

		self.assertEqual(list(result), is_empty)

	# test filter year
	def test_filter_year(self):
		# dummy test
		result = self.entry_class.filter_year('2000', '2002')

	# test generate entry id function
	def test_generate_entry_id(self):
		test_id = self.entry_class.generate_entry_id() - 1
		result = Entry.objects.all().aggregate(Max('entry_id'))
		result = result['entry_id__max']

		self.assertEqual(test_id, result)

		Entry.objects.all().delete()
		test_id = self.entry_class.generate_entry_id()
		result = 1

		self.assertEqual(test_id, result)

	# test get all entries function
	def test_get_all_entries(self):
		second_source_name = 'test2'
		result = self.entry_class.create_new_entry(
			second_source_name,
			self.source_link,
			self.article_title,
			self.publication_date,
			self.author_list,
			self.map_body,
			self.map_scale
		)

		first_entry = {
			'entry_id':self.entry_id,
			'source_name':self.source_name,
			'source_link':self.source_link,
			'article_title':self.article_title,
			'author_list':self.author_list,
			'publication_date':self.publication_date,
			'map_body':self.map_body,
			'map_scale':self.map_scale
		}

		second_entry_id = 2
		second_entry = {
			'entry_id':second_entry_id,
			'source_name':second_source_name,
			'source_link':self.source_link,
			'article_title':self.article_title,
			'author_list':self.author_list,
			'publication_date':self.publication_date,
			'map_body':self.map_body,
			'map_scale':self.map_scale
		}

		result = [first_entry, second_entry]

		test_entries = self.entry_class.get_all_entries()

		self.assertEqual(test_entries, result)

	# test search for keyword function
	def test_search_keyword(self):
		keyword = 'test'
		result = self.entry_class.search_keyword(keyword)

		first_entry = {
			'entry_id':self.entry_id,
			'source_name':self.source_name,
			'source_link':self.source_link,
			'article_title':self.article_title,
			'author_list':self.author_list,
			'publication_date':self.publication_date,
			'map_body':self.map_body,
			'map_scale':self.map_scale
		}

		self.assertEqual([first_entry], result)

		keyword = 'keyword'
		result = self.entry_class.search_keyword(keyword)
		self.assertEqual(None, result)		

	# test verify entry
	def test_verify_entry(self):
		# entry already exists
		result = self.entry_class.verify_entry(
			self.source_name,
			self.source_link,
			self.article_title,
			'2000-01-01',
			self.author_list,
			self.map_body,
			self.map_scale
		)

		self.assertEqual(result, False)

		# good entry
		test_value = 'test2'
		result = self.entry_class.verify_entry(
			test_value,
			self.source_link,
			self.article_title,
			'2000-01-01',
			test_value,
			self.map_body,
			self.map_scale
		)

		self.assertEqual(result, True)

# tests archive class functions
class ArchiveTestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		Archive.objects.all().delete()
		User.objects.all().delete()
		Entry.objects.all().delete()

		# create entry object
		self.entry_id = 1
		self.source_name = 'test'
		self.source_link = 'test'
		self.article_title = 'test'
		self.publication_date = datetime.date(2000, 1, 1)
		self.author_list = 'test'
		self.map_body = 'test'
		self.map_scale = None

		Entry.objects.create(
			entry_id=self.entry_id,
			source_name=self.source_name,
			source_link=self.source_link,
			article_title=self.article_title,
			publication_date=self.publication_date,
			author_list=self.author_list,
			map_body=self.map_body,
			map_scale=self.map_scale
		)

		# create user object
		self.user_id = 1
		# use own test email
		self.email_address = ''
		self.password = 'password1!'
		user_class = UserClass()
		user_class.create_new_user(
			self.email_address,
			self.password
		)
		user_object = User.objects.get(user_id=1)

		# archive class variables
		self.archive_id = 1
		self.keyword = 'test'
		self.frequency = 'month'
		self.entry_number = 1

		# create archive object
		Archive.objects.create(
			user_id=user_object,
			archive_id=self.archive_id,
			keyword=self.keyword,
			frequency=self.frequency,
			entry_number=self.entry_number
		)

		# create class object
		self.archive_class = ArchiveClass()

	# test create new archive function
	def test_create_new_archive(self):
		Archive.objects.all().delete()
		result = self.archive_class.create_new_archive(
			self.archive_id,
			self.keyword,
			self.frequency
		)

		archive_id = Archive.objects.filter(user_id=self.user_id).values(
			'archive_id')
		archive_id = list(archive_id)[0]['archive_id']

		self.assertEqual(result, archive_id)

	# test check entry number function
	def test_check_entry_number(self):
		past_entry_number = 0
		self.archive_class.check_entry_number(
			self.archive_id,
			self.keyword,
			past_entry_number
		)
		result = Archive.objects.filter(archive_id=self.archive_id).values('entry_number')
		result = list(result)[0]['entry_number']

		self.assertEqual(self.entry_number, result)

	# test delete archive function
	def test_delete_archive(self):
		self.archive_class.delete_archive(self.archive_id)
		result = Archive.objects.filter(archive_id=self.archive_id)
		is_empty = []

		self.assertEqual(list(result), is_empty)

	# test generate archive id function
	def test_generate_archive_id(self):
		test_id = self.archive_class.generate_archive_id() - 1
		result = Archive.objects.all().aggregate(Max('archive_id'))
		result = result['archive_id__max']

		self.assertEqual(test_id, result)

		Archive.objects.all().delete()
		test_id = self.archive_class.generate_archive_id()
		result = 1

		self.assertEqual(test_id, result)

	# test get entry number from keyword search
	def test_get_entry_number(self):
		result = self.archive_class.get_entry_number(self.keyword)
		self.assertEqual(result, 1)

		test_keyword = 'abc'
		result = self.archive_class.get_entry_number(test_keyword)
		self.assertEqual(result, 0)

	# test get searches by frequency
	def test_get_searches_by_frequency(self):
		result = self.archive_class.get_searches_by_frequency(self.frequency)
		self.assertEqual(result, [self.archive_id])

		test_frequency = 'week'
		result = self.archive_class.get_searches_by_frequency(test_frequency)
		is_empty = []
		self.assertEqual(result, is_empty)

	# test get all user saved searches
	def test_get_user_saved_searches(self):
		result = self.archive_class.get_user_saved_searches(self.user_id)
		correct_output = [
			{	'user_id_id': self.user_id,
				'archive_id': self.archive_id,
				'keyword': self.keyword,
				'frequency': self.frequency,
				'entry_number': self.entry_number
			}
		]
		self.assertEqual(result, correct_output)

		test_user_id = 2
		result = self.archive_class.get_user_saved_searches(test_user_id)
		is_empty = []
		self.assertEqual(result, is_empty)

	# test run frequency
	def test_run_frequency(self):
		# dummy test
		self.archive_class.run_frequency(self.frequency)

	# test run schedule
	def test_run_schedule(self):
		# dummy test
		self.archive_class.run_schedule()

	# test update frequency
	def test_update_frequency(self):
		new_frequency = 'week'
		self.archive_class.update_frequency(self.archive_id, new_frequency)

		frequency = Archive.objects.filter(archive_id=self.archive_id).values('frequency')
		current_frequency = list(frequency)[0]['frequency']

		self.assertEqual(new_frequency, current_frequency)
