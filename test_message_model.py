import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app
db.create_all()


class MessageModelTestCase(TestCase):
    """ Test cases for message model """

    def setUp(self):
        """ Create test client and a test user """
        db.drop_all()
        db.create_all()

        self.user_id = 99999
        user = User.signup("testusername", "test@email.com", "testpassword", None)
        user.id = self.user_id
        db.session.commit()

        self.user = User.query.get(self.user_id)

        self.client = app.test_client()

    def tearDown(self):
        """ Rollback after testing """
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_add(self):
        """ Testing for adding new message """
        
        message = Message(
            text="Test message",
            user_id=self.user_id
        )

        db.session.add(message)
        db.session.commit()

        self.assertEqual(len(self.user.messages), 1) # 1 message total
        self.assertEqual(self.user.messages[0].text, "Test message") # text of the message equals to Test message

    def test_message_likes(self):
        """ Testing for liking a message """
        message_1 = Message(
            text="Test message 1",
            user_id=self.user_id
        )

        message_2 = Message(
            text="Test message 2",
            user_id=self.user_id 
        )

        user = User.signup("testusernametwo", "testtwo@email.com", "testpasswordtwo", None)
        user_id = 99998
        user.id = user_id
        db.session.add_all([message_1, message_2, user])
        db.session.commit()

        user.likes.append(message_1)

        db.session.commit()

        likes = Likes.query.filter(Likes.user_id == user_id).all()
        self.assertEqual(len(likes), 1)
        self.assertEqual(likes[0].message_id, message_1.id)
