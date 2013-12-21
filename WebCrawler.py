from Class import *
from bs4 import BeautifulSoup
import requests

base_url = "http://www.artsandscience.utoronto.ca/ofr/timetable/winter/"
top_level = "sponsors.htm"

r = requests.get(base_url + top_level)
soup = BeautifulSoup(r.text, 'html5lib')

links = soup.find_all('li')
departments = []
for link in links:
    departments.append(link.a.get("href"))