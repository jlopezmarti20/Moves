import mysql.connector

# Database connection layer of the application

def getDatabase():
    try:
        database = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Moves2026!",
            database="moves_db"
        )

        print("Connected to MySQL!")

        return database

    except mysql.connector.Error as err:
        print(err)
        return None