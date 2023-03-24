from bs4 import BeautifulSoup
import requests
import re
import json


class Scraper:
    url = 'http://bcspcapets.shelterbuddy.com/search/searchResults.asp?task=search&searchid=&advanced=1&s=&rspca_id=&animalType=196%2C197%2C84%2C155%2C2%2C2%2C15%2C3%2C3%2C16%2C158%2C162%2C83%2C80%2C15%2C16%2C86%2C156%2C154%2C159&breed=&breedHidden=&breed2=&breed2Hidden=&colour=&colour2=&sex=&size=1&declawed=&searchType=2&datelostfoundmonth=3&datelostfoundday=9&datelostfoundyear=2023&searchTypeRadio=2&sortBy=&find-submitbtn=Find+Animals'
    
    def scrape(self):
        # r = requests.get(self.url)

        with open('test.html', 'r') as f:
            r = f.read()

        soup = BeautifulSoup(r, 'html.parser')



def parse_animal_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    animals = []
    
    for result in soup.find_all('td', class_='searchResultsCell'):
        animal = {}
        
        # Extract the name
        name_element = result.find('span', class_='searchNameHeading')
        if name_element:
            name_link = name_element.find_next('a')
            animal['name'] = name_link.text if name_link else 'Not found'
        else:
            animal['name'] = 'Not found'
        
        # Extract the color
        color_element = result.find(string='Colour:')
        if color_element:
            color = color_element.next.strip()
            animal['color'] = color
        else:
            animal['color'] = 'Not found'
        
        # Extract the age
        age_element = result.find(string='Age:')
        if age_element:
            age = age_element.next.strip()
            animal['age'] = age
        else:
            animal['age'] = 'Not found'
        
        # Extract the primary breed
        primary_breed_element = result.find(string='Primary Breed:')
        if primary_breed_element:
            primary_breed = primary_breed_element.next.strip()
            animal['primary_breed'] = primary_breed
        else:
            animal['primary_breed'] = 'Not found'
        
        # Extract the secondary breed
        secondary_breed_element = result.find(string='Secondary Breed:')
        if secondary_breed_element:
            secondary_breed = secondary_breed_element.next.strip()
            animal['secondary_breed'] = secondary_breed if secondary_breed != '' else 'Not found'
        else:
            animal['secondary_breed'] = 'Not found'
        
        # Extract the animal sex
        sex_element = result.find(string='Sex:')
        if sex_element:
            sex = sex_element.next.strip()
            animal['sex'] = sex
        else:
            animal['sex'] = 'Not found'
        
        animals.append(animal)

    return animals


new_url = 'http://bcspcapets.shelterbuddy.com/search/searchResults.asp?advanced=1&searchType=2&searchTypeRadio=2&searchTypeId=2&animalType=196%2C197%2C84%2C155%2C2%2C2%2C15%2C3%2C3%2C16%2C158%2C162%2C83%2C80%2C15%2C16%2C86%2C156%2C154%2C159&size=1&datelostfoundmonth=3&datelostfoundday=9&datelostfoundyear=2023&tpage=2&find%2Dsubmitbtn=Find+Animals&pagesize=10&task=view'

# r = requests.get(new_url).text

# with open('new.html', 'w') as f:
#     f.write(r)

with open('new.html', 'r') as f:
    r = f.read()

animals = parse_animal_data(r)

for animal in animals:
    for key, value in animal.items():
        print(f'{key}: {value}')
    print('-----------')
