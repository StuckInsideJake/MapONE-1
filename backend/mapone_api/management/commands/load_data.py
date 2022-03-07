from django.core.management.base import BaseCommand

from mapone_api.entry import EntryClass
from mapone_api.models import Entry

import csv


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		# delete all objects if necessary
		Entry.objects.all().delete()

		entry_class = EntryClass()
		filename = 'data.csv'

		with open(filename) as file:
			reader = csv.reader(file)
			next(reader)

			for line in reader:
				index = 0
				for value in line:
					if value == 'None' or value == '' or value == ' ':
						line[index] = None
					index += 1

				entry_class.verify_entry(
					line[0],
					line[1],
					line[2],
					line[3],
					line[4],
					line[5],
					line[6]
				)
