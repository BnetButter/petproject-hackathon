# Pet Project Hackathon

This is a web application to help address puppy mills in Missouri. To get started with this project, make sure you are running Linux and have docker installed.

Run the following commands:

docker compose build
docker compose up -d


Navigate to http://localhost to navigate to the development server


Here's a breakdown of the directories:

/api-gateway - Code for our backend
/data-scraper - Code for our data scraper that pulls data from https://aphis.my.site.com/PublicSearchTool/s/inspection-reports
/postgis-data - Ignore this directory. Our database volume will be mounted here.
/petproject - Front end application

See here for technical documentation and reporting

https://docs.google.com/document/d/1KGQnDunq8SMWRl2YA_YxbGk2CilJTxqgBqMnPbAAop0/edit?usp=sharing

