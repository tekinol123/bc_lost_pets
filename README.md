# Welcome to my Project
## Project
This project was originally built using Apache Airflow as the orchestration tool but has since been updated to use Azure Data Factory. The web scraping python script and transformation is all done within an Azure function, and that function is triggered via a schedule, currently set to run daily. The data scraped is then uploaded as a CSV file into an Azure Blobk Storage account which is then auto-ingested into a Snowflake table using Azure Event Hubs, Azure Queue Storage, and Snowflake Data Pipelines and Storage Integrations. With the transformed data in a Snowflake table, it is then queried and served via a Flask server, and a Dashboard using Power BI is also available. The link to that dashboard is here: [Power Bi Report](https://app.powerbi.com/view?r=eyJrIjoiOGM3MTRmMjYtODdmMS00NTg2LTkyNTctN2RhZjYyNGIwZmQ1IiwidCI6IjRlZDJhZjZmLWFkNWItNDI3ZC04Yjg5LWM2OGNlOWNjMTdjYiIsImMiOjZ9&pageName=ReportSection)

## API for BC Lost Pets Database  
This API is being served via a flask api. Using this api you can download the pet data directly to analyze the data however you wish. There is no api key required, the API is completely free to use. The api is callable at the url https://api.bcpetsapi.com , the endpoints are below.
### API Calls  
All of the following calls are to be called using a 'get' method.
### Endpoints  
__"/api/all"__: Returns all available pet data    
__"/api/daily"__: Returns pet data retrieved in the last day.  
__"/api/week"__: Returns pet data retrieved in the last 7 days.  
__"/api/month"__: Returns pet data retrieved in the last 30 days.  
__"/api/{Date}"__: Returns pet data retrieved on specified date. Date format is in YYYY-mm-dd and must be after May 24, 2023.  
__"/api/{Start Date}/{End Date}"__: Returns pet data retrieved in the specified time frame. Date format is in YYYY-mm-dd and must be after May 24, 2023.

## Known Issues
One thing I know can be better is the data validation process, as of right now there is now data duplication checking because a lot of the pets dont have names or have generic names so they dont have a unique primary key to identify them by. Another known shortcoming is that the scraper, for some reason only scrapes the first 10 results on the first page of results. I tried editing the URL to change the page number and results per page, but for whatever reason, it still only got the first 10 results. I decided this was okay because we really only wanted the most recent results anyways and there was consistently more than 10 animals listed every day so duplicates are not very common. Going forward, I want to find a way to get all the results and gather additional information such as location found and date found, but that is a problem for another day, this project was done so that I can learn how to create and automate a data pipeline and that is exactly what I achieved and I am happy about that.
