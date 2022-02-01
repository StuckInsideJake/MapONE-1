from django.db import models


class User(models.Model):
	user_id = models.IntegerField(primary_key=True)
	email_address = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)
	
	# need to check
	# SQLite does not support array field
	# string spearated by commas, must convert archive ids into strings
	# and then append
	archive_id_array = models.CharField(max_length=500)

	def __str__(self):
		return self.user_id

class Entry(models.Model):
	entry_id = models.IntegerField(primary_key=True)
	source_name = models.CharField(max_length=100)
	source_link = models.CharField(max_length=300)
	map_area = models.CharField(max_length=100)
	map_scale = models.CharField(max_length=100)
	author_name = models.CharField(max_length=100)

	def __str__(self):
		return self.entry_id

class Archive(models.Model):
	archive_id = models.IntegerField(primary_key=True)
	archive_url = models.CharField(max_length=300)
	frequency = models.CharField(max_length=100)
	entry_number = models.IntegerField()

	def __str__(self):
		return self.archive_id
