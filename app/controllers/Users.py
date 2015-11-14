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

    def index(self):
        return self.load_view('index.html')

    def register(self):
        decide_to_load = self.models['User'].create(request.form)
        print decide_to_load
        if decide_to_load['status']:
            session['user'] = decide_to_load['user'][0]['id'] # store in session
            #use just id - when you need more user info, do a show?
            return self.load_view('success.html', user = decide_to_load['user'][0])

        session['errors'] = decide_to_load['errors']
        return redirect('/')

    def login(self):
        decide_to_load = self.models['User'].login(request.form) #{'status':true/false, 'errors or user':user}
        print decide_to_load
        if decide_to_load['status']:
            session['user'] = decide_to_load['user'][0]['id'] #store in session
            return self.load_view('success.html', user = decide_to_load['user'][0])
        return redirect('/')
