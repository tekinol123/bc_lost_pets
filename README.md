# Welcome to my Project
## TLDR
##### I will be using python's requests and bs4 libraries to scrape the SPCA's lost pets website in British Columbia, Canada. After extracting and cleaning the data using pandas, I will create a data pipeline to have the data fetched on a regular basis to a Snowflake server on Microsoft Azure. Once the data pipeline is made, I will create a dashboard in PowerBI to display my findings about the distributions of where the pets are lost and what species are being lost.

## Inspiration for project
##### I have a friend from British Colombia, Canada who had recently lost their cat. They would tell me about how they would constantly check the BC SPCA website to see if he had been found. I was curious and took a look at the website myself, I noticed that there was lots of lost pets posted every day on that site. So I began to wonder exactly how many pets are lost each day and what the most commonly lost pets are. That gave me the idea for this project, to collect data on these lost pets for a few months and see what the data says.

## The Process
##### I started by creating the python scraper first. I didn't have too much experience with Beautiful Soup prior to this project but I definitely learned alot about it after working with it for this project. The BC SPCA website puts everything as list items but it was still a little bit difficult extracting the exact data I wanted from the tiles as there was data that was sometimes missing. Once I was able to extract the exact soup that I wanted, I had that data put into a pandas dataframe. Pandas is a library I do have experience with already as I use it regularly as a Data Analyst. Once I had the raw extracted data into a pandas dataframe, everything got a lot easier, from there I cleaned the data, filling any blank cells with null data. Another thing I did in pandas was create a new column to convert that age from a string, such as 1Wk or 3Mths into an integer as age_in_days by writing a function and using the pandas "apply" method. I did this so my life would be easier in Power BI and I'm glad I did. Once my scraper was working as intended, I used the azure blob storage python libraries to have my dataframe uploaded as a CSV file to my azure blob container. This was also my first time working with Azure and python but after reading the documentation I was able to figure it out. Okay, I got the software engineering part of the project done, but now began the Data Engineering aspect, I didnt want to manually run this scraper every day and then manually copy that into my Snowflake account every day, so I knew I was going to have to learn some new skills. I decided to go with Apache Airflow for running my script daily, and learned how to use the Azure Event Grid and Azure queue storage for my event notification pipeline. First, I created a storage integration in Snowflake, this part was a little tricky as the documentation can be a little bit unclear at times, however after wrangling with it for a bit I was able to create my external stage, creating the pipeline was the next part, but most of this was done in azure. I followed the documentation and created a queue storage account and a notification integration in Snowflake to receive those event notifications from my Blob storage account. I was really happy to get this working as this was an essential piece to the project. Once that was set up I knew I just had a few steps left before this project was complete. I underestimated this last step as I thought airflow would be pretty straight foward, but I was quickly humbled. After, watching some Youtube videos and generally just tweaking things and seeing what worked, I was able to get my DAG to run as intended. Now came the hard part, getting this thing deployed to Azure. I had to watch several hours of Kubernetes and Docker tutorials but eventually I was able to get the airflow server deployed on Azure kubernetes services and now my project was complete. Just needed to create a Dashboard in Power BI and I was done. I'm really glad I did this project because I learned a lot about data pipelines and how quickly everything can get complex, I know I'm barely scratching the surface with this project but I'm excited to learn more on the next project.
## Known Issues
##### One thing I know can be better is the data validation process, as of right now there is now data duplication checking because a lot of the pets dont have names or have generic names so they dont have a unique primary key to identify them by. Another known shortcoming is that the scraper, for some reason only scrapes the first 10 results on the first page of results. I tried editing the URL to change the page number and results per page, but for whatever reason, it still only got the first 10 results. I decided this was okay because we really only wanted the most recent results anyways and there was consistently more than 10 animals listed every day so duplicates are not very common. Going forward, I want to find a way to get all the results and gather additional information such as location found and date found, but that is a problem for another day, this project was done so that I can learn how to create and automate a data pipeline and that is exactly what I achieved and I am happy about that.