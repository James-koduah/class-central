from pymongo import MongoClient
import uuid
import bcrypt
import requests
import random

class Users():
    """Methods for interacting with the mongodb database"""

    mongo = MongoClient()
    users = mongo.class_central.users



    def create_token(self):
        return str(uuid.uuid4())
    
    def hash_string(self, new_password):
        """Hash the users password"""
        bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        pw = bcrypt.hashpw(bytes, salt)
        return pw.decode('utf8')

    def auth_hashed_string(self, new_value, old_value):
        """Check if the new string(value) matches with the users password"""
        return bcrypt.checkpw(new_value.encode('utf-8'), old_value.encode('utf-8'))

    def signup_user(self, **kwargs):
        email = kwargs.get('email', None)
        password = kwargs.get('password', None)
        check = self.users.find_one({'email': email})
        if check:
            return False
        if not password or len(password) < 8:
            return False
        hashed_password = self.hash_string(password)
        user_id = self.create_token()
        default_hex = [
            "FFCC66",
            "99CCCC",
            "FF9999",
            "CC99FF",
            "4285F4",
            "FF6666",
            "66CCCC",
            "FF9966",
            "5555FF",
            "66CC99"
            ]
        random_hex_color = random.choice(default_hex)
        profile_pic = f'https://eu.ui-avatars.com/api/?name={email[0]}&size=150&color=fff&background={random_hex_color}'

        self.users.insert_one({
            '_id': user_id,
            'email': kwargs['email'],
            'password': hashed_password,
            'profile_pic': profile_pic,
            })
        return user_id

    def login_user(self, **kwargs):
        user = self.users.find_one({'email': kwargs.get('email', None)})
        if not user:
            return None
        
        if kwargs.get('password'):
            # If the user has already created a google account with this email, they will need to reset their password to 
            # use the email method of login
            if user['password'] == None:
                return False
            match = self.auth_hashed_string(kwargs['password'], user['password'])
            if not match:
                return False
            return user

    def get_user(self, id):
        user = self.users.find_one({'_id': id})
        if user:
            return user
        return None
        

        
    def start_db(self):
        config = self.users.find_one({'_id': 'admin'})
        if not config:
            self.users.insert_one({
                '_id': 'admin',
                })

users = Users()
users.start_db()
