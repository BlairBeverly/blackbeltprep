"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)

        self.load_model('Book')
        self.db = self._app.db

   
    def index(self):
        reviews = self.models['Book'].get_recent_reviews()
        all_books_with_reviews = self.models['Book'].get_all_books_with_reviews()

        return self.load_view(
            '/books/index.html', 
            reviews=reviews, 
            all_books_with_reviews=all_books_with_reviews)

    def add(self):
        return self.load_view('/books/addbook.html')

    def add_book_and_review(self):
        data = request.form
        book_id = self.models['Book'].add_book_and_review(
            data, id = session['id'])

        return redirect('/books/' + str(book_id))

    def add_review(self, book_id):
        data = {}
        data['content'] = request.form['content']
        data['rating'] = request.form['rating']
        data['user_id'] = session['id']

        self.models['Book'].add_review(book_id, data)

        return redirect('/books/' + str(book_id))

    def show_book_detail(self, id):
        reviews = self.models['Book'].get_reviews_for_book(id)
        book_info = self.models['Book'].get_book_info(id)

        return self.load_view(
            '/books/addreview.html', 
            reviews = reviews,
            book_info = book_info)

    def delete_review(self, book_id, review_id):
        self.models['Book'].delete_review(review_id)
        return redirect('/books/' + str(book_id))







