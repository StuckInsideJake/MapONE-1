from django.test import TestCase

from mapone_api.user import UserClass
from mapone_api.entry import EntryClass
from mapone_api.archive import ArchiveClass

from mapone_api.models import User, Entry, Archive

from django.db.models import Max


# TODO - API tests too
# tests user class functions
class UserTestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		User.objects.all().delete()

		# class variables
		self.user_id = '1'
		# use own email address
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

	# test  update user email
	def test_update_user_email(self):
		new_email = 'email@email.com'
		self.user_class.change_email(self.user_id, self.email_address,new_email)
		result = User.objects.filter(user_id=self.user_id).values('email_address')
		result = list(result)[0]['email_address']

		self.assertEqual(new_email, result)

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

	# test verify email address
	# RUN TEST BY ITSELF --> ISSUES W API
	# def test_verify_email_address(self):
	# 	result = self.user_class.verify_email_address(self.email_address)
	# 	self.assertEqual(result, False)
		
	# 	test_email = 'abc'
	# 	result = self.user_class.verify_email_address(test_email)
	# 	self.assertEqual(result, False)

	# 	API doesn't allow multiple tests @ a time but test works
	#	# use own test email
	# 	test_email = ''
	# 	result = self.user_class.verify_email_address(test_email)
	# 	self.assertEqual(result, True)

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



# TODO - API tests too
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
		self.author_list = 'abc,def,ghi jk'
		self.planet_flag = True
		self.planet_name = 'test'
		self.region_name = 'test'
		self.map_scale = None

		# create database object
		Entry.objects.create(
			entry_id=self.entry_id,
			source_name=self.source_name,
			source_link=self.source_link,
			article_title=self.article_title,
			author_list=self.author_list,
			planet_flag=self.planet_flag,
			planet_name=self.planet_name,
			region_name=self.region_name,
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
			self.author_list,
			self.planet_flag,
			self.planet_name,
			self.region_name,
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
			self.author_list,
			self.planet_flag,
			self.planet_name,
			self.region_name,
			self.map_scale
		)

		first_entry = {
			'entry_id':self.entry_id,
			'source_name':self.source_name,
			'source_link':self.source_link,
			'article_title':self.article_title,
			'author_list':self.author_list,
			'planet_flag':self.planet_flag,
			'planet_name':self.planet_name,
			'region_name':self.region_name,
			'map_scale':self.map_scale
		}

		second_entry_id = 2
		second_entry = {
			'entry_id':second_entry_id,
			'source_name':second_source_name,
			'source_link':self.source_link,
			'article_title':self.article_title,
			'author_list':self.author_list,
			'planet_flag':self.planet_flag,
			'planet_name':self.planet_name,
			'region_name':self.region_name,
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
			'planet_flag':self.planet_flag,
			'planet_name':self.planet_name,
			'region_name':self.region_name,
			'map_scale':self.map_scale
		}

		self.assertEqual([first_entry], result)

		keyword = 'test keyword'
		result = self.entry_class.search_keyword(keyword)
		self.assertEqual(None, result)		

	# test verify entry
	def test_verify_entry(self):
		# entry already exists
		result = self.entry_class.verify_entry(
			self.source_name,
			self.source_link,
			self.article_title,
			self.author_list,
			self.planet_flag,
			self.planet_name,
			self.region_name,
			self.map_scale
		)

		self.assertEqual(result, False)

		# need to wait on client response --> see entry class
		# # entry does not have minimum requirements
		# result = self.entry_class.verify_entry(
		# 	None,
		# 	None,
		# 	None,
		# 	None,
		# 	None,
		# 	None,
		# 	None,
		# 	None
		# )

		# self.assertEqual(result, False)

		# good entry
		test_value = 'test2'
		result = self.entry_class.verify_entry(
			test_value,
			self.source_link,
			self.article_title,
			test_value,
			self.planet_flag,
			self.planet_name,
			self.region_name,
			self.map_scale
		)

		self.assertEqual(result, True)


# TODO - API tests too
# tests archive class functions
class ArchiveTestCase(TestCase):

	# test constructor
	def setUp(self):
		# delete all objects for testing purposes
		Archive.objects.all().delete()
		User.objects.all().delete()

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
		self.entry_number = 10

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
