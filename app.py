import streamlit as st
import pymongo
import psycopg2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

channel_id_options = ['UCduIoIMfD8tT3KoU0-zBRgQ', # Guvi Sharing
                        'UCiEmtpFVJjpvdhsQ2QAhxVA', # ZenClass from Guvi 
                        'UCOrS4ObeJ08FmsVG9Fwhmsg', # busy funda
                        'UCPx4S2RcDCJmP_ht9CgFiVQ', # Simply Waste
                        'UCEbrPQG7gvhl34vhAAu1nWw', # Days of fact
                        'UCZNJwsk57AQIupUXDQcA9qg', # Travel Tech Hari
                        'UCqZJHBjPjCl3dk2PSbAdpnw', # Payasam
                        'UCo33niDKpTpgwZ_dohqvylg', # Tube Buddy
                        'UCR5k7bm0qgpP7-QX1uIx7cQ', # grow your gaming channel
                        'UCE4Gn00XZbpWvGUfIslT-tA' # Magnates Media
              ]



# Connect to MongoDB
def connect_to_mongodb():
    client = pymongo.MongoClient('mongodb+srv://satheeshkumar147:test@satheeshkumar147.u7xeukv.mongodb.net/?retryWrites=true&w=majority')
    db = client["youtube_database"]
    return db

# Connect to PostgreSQL
def connect_to_postgresql():
    conn = psycopg2.connect(
        host="localhost",
        database="youtube_db",
        user="postgres",
        password="123"
    )

    cursor = conn.cursor()
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'channels'
          AND column_name = 'subscriber_count';
    """)
    
    if cursor.fetchone() is None:
        cursor.execute("""
            ALTER TABLE channels
            ADD COLUMN subscriber_count INTEGER;
        """)
        conn.commit()
    
    cursor.close()

    return conn

# Fetch and store channel details in MongoDB
def fetch_channel_details(channel_id, youtube_api_key):
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    try:
        response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        ).execute()

        channel_data = response["items"][0]

        db = connect_to_mongodb()
        collection = db["channel_data"]
        collection.insert_one(channel_data)

        st.success("Channel details stored in MongoDB successfully.")

    except HttpError as e:
        st.error("An error occurred:", e)


# Migrate data from MongoDB to PostgreSQL
def migrate_data():
    db = connect_to_mongodb()
    conn = connect_to_postgresql()
    collection = db["channel_data"]
    data = collection.find()

    cursor = conn.cursor()
    for doc in data:
        channel_name = doc["snippet"]["title"]
        subscriber_count = doc["statistics"]["subscriberCount"]
        video_count = doc["statistics"]["videoCount"]

        cursor.execute(
            "INSERT INTO channels (channel_name, subscriber_count, video_count) VALUES (%s, %s, %s)",
            (channel_name, subscriber_count, video_count)
        )

    conn.commit()
    cursor.close()
    conn.close()

    st.success("Data migration completed.")

# Retrieve channel details from PostgreSQL
def retrieve_data():
    conn = connect_to_postgresql()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM channels")
    data = cursor.fetchall()

    st.header("Channel Details")
    for row in data:
        channel_name = row[2]
        subscriber_count = row[5]
        video_count = row[4]

        st.subheader(channel_name)
        st.write(f"subscriber_count: {subscriber_count}")
        st.write(f"Videos: {video_count}")
        

    cursor.close()
    conn.close()

# Streamlit app
def main():
    st.title("YouTube Channel Data Migration")

    # Input fields
    channel_id = st.selectbox("Enter YouTube Channel ID:", channel_id_options)
    youtube_api_key = 'AIzaSyBWiZDqp19HN8dg1Cznr-w0Q2PRHoTZ6Nc'

    # Fetch button
    if st.button("Fetch Channel Details"):
        if channel_id and youtube_api_key:
            fetch_channel_details(channel_id, youtube_api_key)
        else:
            st.warning("Please enter Channel ID and API Key.")

    # Migrate button
    if st.button("Migrate Data"):
        migrate_data()

    # Retrieve button
    if st.button("Retrieve Data"):
        retrieve_data()

if __name__ == "__main__":
    main()
