import schedule

from mapone_api.archive import ArchiveClass


# call archive 
archive_class = ArchiveClass()

# set time
midnight = '00:00'

# run schedule daily
schedule.every().day.at(midnight).do(archive_class.run_schedule())

# internal timer
while True:
	schedule.run_pending()
	time.sleep(1)
