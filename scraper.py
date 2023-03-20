import bs4
import requests
import re
import json


class Scraper:
    url = 'http://bcspcapets.shelterbuddy.com/search/searchResults.asp?task=search&searchid=&advanced=1&s=&rspca_id=&animalType=196%2C197%2C84%2C155%2C2%2C2%2C15%2C3%2C3%2C16%2C158%2C162%2C83%2C80%2C15%2C16%2C86%2C156%2C154%2C159&breed=&breedHidden=&breed2=&breed2Hidden=&colour=&colour2=&sex=&size=1&declawed=&searchType=2&datelostfoundmonth=3&datelostfoundday=9&datelostfoundyear=2023&searchTypeRadio=2&sortBy=&find-submitbtn=Find+Animals'
        
    def scrape(self):
        # r = requests.get(self.url)

        with open('test.html', 'r') as f:
            r = f.read()

        soup = bs4.BeautifulSoup(r, 'html.parser')
        soup = soup.select('.searchNameHeading')
        
        return soup

test = Scraper().scrape()
test = list(test)