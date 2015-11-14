"""
    Sample Model File

    A Model should be in charge of communicating with the Database.
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
import re
from system.core.model import Model

class User(Model):

    def __init__(self):
        super(User, self).__init__()

    def show(self, params):
        pass
    def show_by_email(self,params):
        query = "SELECT * FROM users where email = '{}'".format(params)
        return self.db.query_db(query)

    def login (self, params):
        user = self.show_by_email(params['email'])
        if len(user)>0:
            if self.bcrypt.check_password_hash(user[0]['password'], params['password']):
                return {'status':True, "user":user}
        return {'status':False}


    def create(self,params):
        #info = request.from from register.
        print 'IN CREATE'
        is_valid = self.validation(params) #{'status':True (or False), 'errors':[]}
        if is_valid['status']:
            print "IS VALID"
            bcrypt_password = self.bcrypt.generate_password_hash(params['password'])
            query = "insert into users (first_name, last_name, password, email, created_at, updated_at) values ('{}', '{}', '{}', '{}', now(),now())".format(params['first_name'], params['last_name'], bcrypt_password,params['email'])
            self.db.query_db(query)
            return {'status':True, "user":self.show_by_email(params['email'])} #whole thing: dictionary with a list with dictionary (length 1 hopefully)
        else:
            print "NOT VALID"
            return is_valid #{'status':False, "errors":errors}

    #validations helper function
    def validation(self, params):
        #print "IN VALIDATION"
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        is_present_in_db = self.show_by_email(params['email']); #[{}] list with dictionary


        if len(is_present_in_db) > 0:
            print "not valid", is_present_in_db
            errors.append('user already exists')
            return {"status": False, "errors": errors}
        # Some basic validation

        if not params['first_name']:
            errors.append('first name cannot be blank')
        elif len(params['first_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not params['last_name']:
            errors.append('last name cannot be blank')
        elif len(params['last_name']) < 2:
            errors.append('Name must be at least 2 characters long')
        print "IN VALIDATION"
        print params
        if not params['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(params['email']):
            errors.append('Email format must be valid!')
        if not params['password']:
            errors.append('Password cannot be blank')
        elif len(params['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif params['password'] != params['pw_repeat']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            print "ERRORS"
            return {"status": False, "errors": errors} #don't create user because there are errors.
        print "NO ERRORS"
        return {'status': True} # can create user
