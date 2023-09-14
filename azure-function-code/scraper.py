from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from datetime import datetime
import pytz

class Scraper:
    def __init__(self):
        self.site_url = 'http://bcspcapets.shelterbuddy.com/search/searchResults.asp?task=search&searchid=&advanced=1&s=&rspca_id=&animalType=196%2C197%2C84%2C155%2C2%2C2%2C15%2C3%2C3%2C16%2C158%2C162%2C83%2C80%2C15%2C16%2C86%2C156%2C154%2C159&breed=&breedHidden=&breed2=&breed2Hidden=&colour=&colour2=&sex=&size=1&declawed=&searchType=2&datelostfoundmonth=3&datelostfoundday=9&datelostfoundyear=2023&searchTypeRadio=2&sortBy=&find-submitbtn=Find+Animals'


    def scrape(self):
        r = requests.get(self.site_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def parse_animal_data(self):
        soup = self.scrape()
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
                animal['sex '] = 'Not found'
            
            animals.append(animal)

        return pd.DataFrame(animals)

def duration_to_days(duration_string):
        # Define conversion factors for years, months, and weeks
    conversion_factors = {
        'Yrs': 365,
        'Mths': 30,
        'Wks': 7
    }

    # Define the regex pattern to match the duration string
    regex_pattern = r"(\d+)\s*(Yrs|Mths|Wks)"
    match = re.search(regex_pattern, duration_string)

    if match:
        # Extract the number and unit from the match
        number = int(match.group(1))
        unit = match.group(2)

        # Convert the duration to days
        days = number * conversion_factors[unit]
        return days
    else:
        return None
    