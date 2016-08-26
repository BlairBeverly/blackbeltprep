""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()


    def get_recent_reviews(self):
        query = "SELECT b.title as title, r.book_id AS book_id, r.content as "\
                " content, r.rating as rating, u.name as username, r.added_on as "\
                " added_on FROM reviews r JOIN books b ON (r.book_id = b.id) JOIN "\
                " users u ON (r.user_id = u.id) ORDER BY r.id DESC LIMIT 3"
        return self.db.query_db(query)

    def get_all_books_with_reviews(self):
        query = "SELECT title, id FROM books"
        return self.db.query_db(query)

    def add_book_and_review(self, data, id):
        print data

        query1 = "INSERT INTO books (title, author, added_on, updated_on) " \
                "VALUES (:title, :author, NOW(), NOW())"

        if data['existing_author'] != '':
            author = data['existing_author']
        else:
            author = data['new_author']

        query1_data = {'title': data['title'],
                'author': author}

        inserted_book_id = self.db.query_db(query1, query1_data)

        query2_data = {'content': data['content'],
               'rating': data['rating'],
               'user_id': id,
               'book_id': inserted_book_id}

        self.add_review(inserted_book_id, query2_data)

        return inserted_book_id

    def add_review(self, book_id, review_info):
        query = "INSERT INTO reviews (content, rating, added_on, updated_on, "\
        "user_id, book_id) VALUES (:content, :rating, NOW(), NOW(), "\
        ":user_id, :book_id)"

        data = {'content': review_info['content'],
                'rating': review_info['rating'],
                'user_id': review_info['user_id'],
                'book_id': book_id}


        self.db.query_db(query, data)



    def get_reviews_for_book(self, id):
        query = "SELECT r.id as id, r.user_id as user_id, rating, content, "\
                "name, r.added_on as added_on FROM reviews r JOIN users "\
                "u ON r.user_id = u.id WHERE book_id = :id"

        data = {'id': id}

        return self.db.query_db(query, data)

    def get_book_info(self, id):
        query = "SELECT * FROM books where id = :id"
        data = {'id': id}

        return self.db.get_one(query, data)

    def delete_review(self, review_id):
        query = "DELETE FROM reviews WHERE id = :review_id"
        data = {'review_id': review_id}

        self.db.query_db(query, data)


    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """