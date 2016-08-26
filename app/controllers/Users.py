"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

   
    def index(self):
        return self.load_view('/users/welcome.html')

    
    def register(self):
        info = {'name': request.form['name'],
                'alias': request.form['alias'],
                'email': request.form['email'],
                'password': request.form['password'],
                'password_conf': request.form['password_conf']}

        response = self.models['User'].register_user(info)

        if 'errors' in response:
            for error in response['errors']:
                flash(error)
            return redirect('/')
        
        else:
            session['name'] = info['name']
            session['id'] = response['user_id']
            return redirect('/books')

    def login(self):
        info = {'email': request.form['email'], 
                'password': request.form['password']}

        response = self.models['User'].login_user(info)

        print 'ID HERE ->>>>>', response.id

        if 'errors' in response:
            for error in response['errors']:
                flash(error)
            return redirect('/')

        else:
            session['name'] = response.name
            session['id'] = response.id
            return redirect('/books')

    def get_user_info(self, id):
        user_info, review_count, books_reviewed = \
        self.models['User'].get_user_info(id)

        return self.load_view(
            '/users/userdetail.html', 
            user_info = user_info,
            review_count = review_count,
            books_reviewed = books_reviewed)











