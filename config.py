from dotenv import load_dotenv
from os import getenv
from pymongo import MongoClient

load_dotenv()

# Load all the api keys and config variables
discord_token = getenv("DISCORD_TOKEN")
google_search_api_key = getenv("GOOGLE_SEARCH_API_KEY")
search_engine_id = getenv("SEARCH_ENGINE_ID")

# initiate MongoDB Atlas connection
client = MongoClient(getenv("MONGO_URI"))
db = client.discordBot
