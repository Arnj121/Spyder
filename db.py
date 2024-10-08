from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

dburl=os.getenv('LOCALURL')
host=os.getenv('HOST')
vidport=os.getenv('VIDPORT')
imgport=os.getenv('IMGPORT')
audport=os.getenv('AUDPORT')
textport=os.getenv('TEXTPORT')
searchport=os.getenv("SEARCHPORT")
database=os.getenv('DATABASE')
collecName=os.getenv('COLLECNAME')


client = MongoClient(dburl)
db = client[database]
collection = db[collecName]
