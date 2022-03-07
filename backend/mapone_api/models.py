from django.db import models

class User(models.Model):
	user_id = models.IntegerField(primary_key=True)
	email_address = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)

	def __str__(self):
		return str(self.user_id)

class Entry(models.Model):
	entry_id = models.IntegerField(primary_key=True)
	source_name = models.CharField(max_length=100)
	source_link = models.CharField(max_length=300)
	article_title = models.CharField(max_length=100)
	publication_date = models.DateField()
	author_list = models.CharField(max_length=100)
	map_body = models.CharField(max_length=100)
	map_scale = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.entry_id)

class Archive(models.Model):
	user_id = models.ForeignKey(
		User,
		to_field='user_id',
		on_delete=models.CASCADE
	)
	archive_id = models.IntegerField(primary_key=True)
	keyword = models.CharField(max_length=100, unique=True)
	frequency = models.CharField(max_length=100)
	entry_number = models.IntegerField()

	def __str__(self):
		return str(self.archive_id)
