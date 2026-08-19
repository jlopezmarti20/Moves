
import re

def createAccount(database, username, email, password):
    # cursor is responsible for executing SQL statements
    cursor = database.cursor()

    #check for valid email format
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        return database, False

    # Check if account already exists
    cursor.execute(
        'SELECT * FROM users WHERE email = %s', (email, )
    )
    account = cursor.fetchone()
    if account: 
        cursor.close()
        return database, False
    else:
        # Adding account to both account and favorites table
        cursor.execute( 'INSERT INTO users'
            '(username, email, password)'
            'VALUES (%s, %s, SHA2(%s, 512))',
            (username, email, password, ))

        # cursor.execute('INSERT INTO favorites'
        #                '(email)'
        #                'VALUES (%s)',
        #                (email,))
        database.commit()
        cursor.close()
        return database, True



def login(database, email, password):
    cursor = database.cursor(dictionary=True)

    # Check if the email is valid
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        print("Invalid email")
        cursor.close()
        return database, None

    #Getting user from database
    cursor.execute(
        'SELECT id, username, email FROM users WHERE email = %s AND password = SHA2(%s, 512)',
        (email, password, )
    )
    user = cursor.fetchone()
    
    #Returns if email is tied to user account
    cursor.close()
    return database, user



def getUserByEmail(database, email):
    ...


def deleteUser(database, user_id):
    ...


def saveBookmark(database, user_id, place):
    cursor = database.cursor()

    # Check if this bookmark already exists
    cursor.execute(
        """ 
        SELECT id FROM favorites where user_id =%s AND place_id = %s

        """, (user_id, place["place_id"])
    )

    if cursor.fetchone():
        cursor.close()
        return database, False

    cursor.execute(
        '''
        INSERT INTO favorites
        (user_id,
         place_id,
         name,
         address,
         rating,
         image,
         categories,
         distance_miles)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
        ''',
        (
            user_id,
            place["place_id"],
            place["name"],
            place["address"],
            place["rating"],
            place["image"],
            place["categories"],
            place["distance_miles"]
        )
    )

    database.commit()
    cursor.close()

    return database, True




def getBookmarks(database, user_id):
    cursor = database.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM favorites
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    bookmarks = cursor.fetchall()
    cursor.close()

    return database, bookmarks

def removeBookmark(database, user_id, place_id):
    cursor = database.cursor()

    cursor.execute(
        """
        DELETE FROM favorites
        WHERE user_id = %s
        AND place_id = %s

        """,
        (user_id, place_id)
    )
    database.commit()
    cursor.close()

    return database, True

