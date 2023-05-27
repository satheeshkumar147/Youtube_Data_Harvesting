# Youtube_Data_Harvesting

Domain : Social Media

Problem Statement :

The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. Extracting data using Youtube API and storing it on MongoDB then Transforming it to a relational databaselike PostgreSQL. For getting various info about youtube channels.

Technologies used :

Python
MongoDB
PostgreSQL
YouTube Data API
Streamlit
Pandas

Overview :

This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a MongoDB database, migrates it to a SQL data warehouse, and enables users to search for channel details and join tables to view data in the Streamlit app.

Workflow :

Connect to the YouTube API this API is used to retrieve channel, videos, comments data. I have used the Google API client library for Python to make requests to the API.

The user will able to extract the Youtube channel's data using the Channel ID. Once the channel id is provided the data will be extracted using the API.

Once the data is retrieved from the YouTube API, it is stored it in a MongoDB as data lake. MongoDB is a great choice for a data lake because it can handle unstructured and semi-structured data easily.

After collected data for multiple channels,it is then migrated/transformed it to a structured PostgreSQL as data warehouse.

Then used SQL queries to join the tables in the SQL data warehouse and retrieve data for specific channels based on user input.

Finally, the retrieved data is displayed in the Streamlit app

Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing it in a MongoDB data lake, migrating it to a SQL data warehouse, querying the data warehouse with PostgreSQL, and displaying the data in the Streamlit app.
