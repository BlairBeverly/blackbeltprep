
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def login_user(self, info):
        query = "SELECT name, id, hash_pw FROM users WHERE email = :email"
        data = {'email': info['email']}

        errors = []

        user = self.db.get_one(query, data)

        if user:
            if self.bcrypt.check_password_hash(user.hash_pw, info['password']):
                return user
            else:
                errors.append('Invalid password')
        else: 
            errors.append('Invalid email')

        return {'errors': errors, 'user_id': user[0]['id']}


    def register_user(self, info):
        EMAIL_REGEX = re.compile(
            r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

        errors = []

        if not info['name']:
            errors.append('Must include first name')
        if len(info['name']) < 2:
            errors.append('First name must be at least two characters')
        if not info['alias']:
            errors.append('Must include alias')
        if len(info['alias']) < 2:
            errors.append('Last name must be at least two characters')
        if not re.match(EMAIL_REGEX, info['email']):
            errors.append('Must be valid email')
        if len(info['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if info['password'] != info['password_conf']:
            errors.append('Password did not match password confirmation')

        if errors:
            return {'status': 'error', 'errors': errors}
        else:
            query = "INSERT INTO users (name, alias, email, hash_pw, "\
                    " added_on, updated_on) VALUES (:name, :alias, "\
                    ":email, :hash_pw, NOW(), NOW())"

            hash_pw = self.bcrypt.generate_password_hash(info['password'])
            data = {'name': info['name'],
                    'alias': info['alias'],
                    'email': info['email'],
                    'hash_pw': hash_pw}

            user_id = self.db.query_db(query, data)

            return {'status': 'ok', 'user_id':user_id}

    def get_user_info(self, id):
        query1 = "SELECT * FROM Users WHERE id = :id"
        data = {'id': id}

        query2 = "SELECT COUNT(*) as count FROM reviews where user_id = :id"
        query3 = "SELECT b.title as title, b.id as id FROM reviews r JOIN books b ON "\
                 "r.book_id = b.id WHERE user_id = :id GROUP BY 1,2"

        user_info = self.db.get_one(query1, data)
        review_count = self.db.get_one(query2, data)
        books_reviewed = self.db.query_db(query3, data)

        return (user_info, review_count, books_reviewed)












