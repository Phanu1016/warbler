import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """ Test cases for user views """

    def setUp(self):
        """ Create test client and test users """

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user_one = User.signup("testuserone", "testuserone@email.com", "testuserone", None)
        self.user_one_id = 9999
        self.user_one.id = self.user_one_id

        db.session.commit()

    def tearDown(self):
        """ Rollback after testing """
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_user_detail(self):
        """ Test user detail page """
        with self.client:
            response = self.client.get('/users/9999')
            html = response.get_data(as_text=True)
            self.assertIn('@testuserone', html)