import mysql.connector
import hashlib

class UserDataBase:
    def __init__(self) -> None:
        try:
            # Establish a connection to the MySQL database
            self.cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='auth', port=3306)
            # Create a cursor for executing queries
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as e:
            # Handle database connection errors
            print(f"Error connecting to the database: {e}")
            raise
    
    def __del__(self):
        # Ensure that the database connection is closed when the object is deleted
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'cnx') and self.cnx:
            self.cnx.close()

    def get_user(self, user_id: int):
        try:
            # Retrieve user information from the database based on user ID
            query = "SELECT * FROM user WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            res = self.cursor.fetchone()
            if res:
                # Map database result to a dictionary for better readability
                user_dic = {
                    "id": res[0],
                    "Username": res[1],
                    "Email": res[2],
                    "U_password": res[3],
                    "Role": res[4]
                }
                return user_dic
            else:
                # Raise a custom exception if the user is not found
                raise UserNotFoundException(f"User with ID {user_id} not found")
        except mysql.connector.Error as e:
            print(f"Error retrieving user: {e}")
            raise

    def add_user(self, user_info):
        try:
            # Hash the user password before storing it in the database
            user_password = hashlib.sha256(user_info["U_password"].encode('utf-8')).hexdigest()
            query = "INSERT INTO USER (USERNAME, EMAIL,  U_PASSWORD, U_ROLE) VALUES (%s, %s, %s, %s)"
            values = (user_info['Username'], user_info['Email'], user_password, user_info['Role'])
            self.cursor.execute(query, values)
            # Commit the changes to the database
            self.cnx.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error adding user: {e}")
            # Log the exception or handle specific database-related exceptions
            raise

    def delete_user(self, user_id):
        try:
            # Delete a user from the database based on user ID
            query = "DELETE FROM user WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            if self.cursor.rowcount == 0:
                # Return False if no rows were affected (user not found)
                return False
            else:
                # Commit changes if the user was successfully deleted
                self.cnx.commit()
                return True
        except mysql.connector.Error as e:
            print(f"Error deleting user: {e}")
            raise

    def verify_user(self, user_cred):
        try:
            # Verify user credentials (username and hashed password) from the database
            username = user_cred["Username"]
            password = hashlib.sha256(user_cred["U_password"].encode('utf-8')).hexdigest()
            query = "SELECT id FROM User WHERE username = %s AND u_password = %s"
            values = (username, password)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                # Return the user ID if the credentials are valid
                return result[0]
        except mysql.connector.Error as e:
            print(f"Error verifying user: {e}")
            raise

        
# Custom exception for user not found
class UserNotFoundException(Exception):
    pass