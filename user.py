# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    DB = "users"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    # Now we use class methods to query our database
    # And perform input validations

    @classmethod
    def is_valid_user(cls, user):
        is_valid = True

        if len(user["first_name"]) <= 0:
            is_valid = False
            flash("First name is required.")
        if len(user["last_name"]) <= 0:
            is_valid = False
            flash("Last name is required.")
        if len(user["email"]) <= 0:
            is_valid = False
            flash("Email is required.")

        if len(user["email"]) > 0 and not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email format.")
            is_valid = False

        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.DB).query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data):
        query = """
        INSERT into users (first_name, last_name, email) VALUES 
        (%(first_name)s, %(last_name)s, %(email)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)