import requests
import re
import csv
from bs4 import BeautifulSoup

# Link to source used for scraping
url = "https://link.springer.com/article/10.1186/s40645-020-0323-9"

# Requests module use to data from given url (loading url)
result = requests.get(url)

# Used for getting HTML structure from requests response (parsing text from html doc)
doc = BeautifulSoup(result.content, "html.parser")

"""Begin Scraping"""

# Finds the title of article/publication in Springer library
title = doc.find('h1', {'class':'c-article-title'})
print("=====Title of Abstract=====")
print(title.string + "\n")

# Finds the author(s) of article/publication in Springer library
author = ''.join(str(author) for author in [authorElement.text for authorElement in doc.findAll('li', {'class':'c-article-author-list__item'})])
print("=====Author(s) of Abstract=====")
print(author + "\n")

# Finds the date of article/publication in Springer library
abstract_date = doc.find('time').get('datetime')
print("=====Publication Date=====")
print("This abstract was published on: " + abstract_date + "\n")

# Finds and displays the content in the abstract section of the publication
abstract = str(doc.find('div', {'id':'Abs1-content'}).text.encode('utf-8'))[1:]
print("=====Primary Abstract Content=====")
print(abstract)

# Future use to write print statements to csv file for database
with open('scraper_data.csv', 'wb') as file:
    writer = csv.writer(file)
    for line in open('mapScraper.py'):
        rec = line.strip()
        if rec.startswith('PLY'):
            writer.writerow(rec.split(','))

#tags = doc.find_all(["a", "p", "tr"], text="")
#print(tags)

#links = doc.find_all('a', href=re.compile(r'(.pdf)'))
#print(links)

# Finds all html <a> tags (modify class to be html class name)
#links = BeautifulSoup.find_all('a', href=True, class_='')
#for link in links:
#    print(link['href'])

# Finds div holding source text (modify class to be html class name)
#BeautifulSoup.find('div', class_='').get_text()
