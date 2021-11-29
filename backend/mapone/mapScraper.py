import requests
from bs4 import BeautifulSoup

# Link to source used for scraping
url = "https://www.sciencedirect.com/science/article/pii/S0377027320302523"

# Requests module use to data from given url
result = requests.get(url)

# Used for getting HTML structure from requests response
doc = BeautifulSoup(result.text, "html.parser")

title = doc.find_all("h1")
print(title)

# Finds all html <a> tags (modify class to be html class name)
links = BeautifulSoup.find_all('a', href=True, class_='')
for link in links:
    print(link['href'])

# Finds div holding source text (modify class to be html class name)
BeautifulSoup.find('div', class_='').get_text()
