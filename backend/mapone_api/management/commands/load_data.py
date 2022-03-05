from django.core.management.base import BaseCommand

from mapone_api.entry import EntryClass

import csv


class Command(BaseCommand):

	def handle(self, *args, **kwargs):
		entry_class = EntryClass()
		filename = 'data.csv'

		with open(filename) as file:
			reader = csv.reader(file)
			next(reader)

			for line in reader:

				entry_class.verify_entry(
					line[0],
					line[1],
					line[2],
					line[3],
					line[4],
					line[5],
					line[6]
				)
