from connection import getDatabase

database = getDatabase()

if database:
    print("Connection successful!")
else:
    print("Connection failed!")