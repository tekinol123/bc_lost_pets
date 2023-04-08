from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import io

load_dotenv()

connection_string = f"DefaultEndpointsProtocol=https;AccountName={os.environ['STORAGE_ACCOUNT_NAME']};AccountKey={os.environ['STORAGE_ACCOUNT_KEY']};EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Reference the container
container_name = os.environ['CONTAINER_NAME']
container_client = blob_service_client.get_container_client(container_name)

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


new_url = 'http://bcspcapets.shelterbuddy.com/search/searchResults.asp?advanced=1&searchType=2&searchTypeRadio=2&animalType=196%2C197%2C84%2C155%2C2%2C2%2C15%2C3%2C3%2C16%2C158%2C162%2C83%2C80%2C15%2C16%2C86%2C156%2C154%2C159&size=1&sortBy=1&datelostfoundmonth=3&datelostfoundday=9&datelostfoundyear=2023&find-submitbtn=Find+Animals&pagesize=75&task=view&searchTypeId=2&tpage=1'

r = requests.get(new_url).text

# with open('new.html', 'r') as f:
    # r = f.read()

animals = parse_animal_data(r)

animals_df = pd.DataFrame(animals)

#Cleaning Data
pattern = r"\s*\(\s*approx\s*\)\s*"
animals_df['age'] = animals_df['age'].replace(pattern, '', regex=True)
animals_df['age_in_days'] = animals_df['age'].apply(duration_to_days)
# Reset the index and update the original DataFrame
# animals_df.reset_index(drop=True, inplace=True)

# animals_df.fillna('Not found', inplace=True)


csv_file = io.BytesIO()
animals_df.to_csv(csv_file, index=False, mode='w', header=True, encoding='utf-8')
csv_file.seek(0)

blob_name = f'{datetime.now().date()}_animals.csv'
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(csv_file, overwrite=True)

# animals_df.to_csv('animals.csv', index=False, mode='a', header=False)
# animals_df.to_csv(f'./data/{datetime.now().date()}_animals.csv', index=False, mode='w', header=True)
# Next we need to install apache airflow and set this script to run daily. we also need to to fix the script so that it gets data on every page
