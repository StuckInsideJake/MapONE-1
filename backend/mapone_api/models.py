from django.db import models

class Publication(models.Model):
	source = models.CharField(max_length=100)
	link = models.CharField(max_length=200)
	body = models.CharField(max_length=100)
	scale = models.CharField(max_length=100)
	author = models.CharField(max_length=100)

	# TODO - need clarity on this field
	publication_info = models.CharField(max_length=100)

	def __str__(self):
		return self.source
