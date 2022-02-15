# Importing pre_processing() which generates LOG files during the code run
from common_functions import pre_processing

# Importing the scraper_main() which initiates the scraping process
from scraperV2 import scraper_main

# Abstracts containing these keywords will be scraped from Springer
'''INSERT KEYWORDS HERE'''
keywords_to_search = "Pavonis Mons Mars"

# References a separate LOG folder that holds abstract names and status of each one
abstracts_log_name, status_logger_name = pre_processing(keywords_to_search)

# Calling the scraper_main() to start the scraping process
scraper_main(keywords_to_search, abstracts_log_name, status_logger_name)