import pytest
from test import email, delighted
from datetime import datetime, timedelta
from time import mktime


class TestCreatePerson(object):

    def now(self):
        return datetime.now()

    def addSeconds(self, date_time, seconds):
        return date_time + timedelta(seconds=seconds)

    def assert_between(self, date_time, start, end):

        assert (date_time >= mktime(start.timetuple()))
        assert (date_time <= mktime(end.timetuple()))

    def test_send_without_delay(self, delighted, email):

        start = self.now()

        later = self.addSeconds(start, 5)

        response = delighted.people.create(email=email, delay=0)

        assert response['email'] == email
        assert response['id']
        assert response['name'] is None
        assert response['properties'] == {}
        self.assert_between(response['survey_scheduled_at'], start, later)

    def test_send_with_delay(self, delighted, email):

        start = self.now()

        later = self.addSeconds(start, 15)

        response = delighted.people.create(email=email, delay=10)

        assert response['email'] == email
        assert response['id']
        assert response['name'] is None
        assert response['properties'] == {}
        self.assert_between(response['survey_scheduled_at'], start, later)

    def test_do_not_send(self, delighted, email):

        response = delighted.people.create(email=email, send=False)

        assert response['email'] == email
        assert response['id']
        assert response['name'] is None
        assert response['properties'] == {}
        assert response['survey_scheduled_at'] is None


class TestDeletePerson(object):

    def test_delete_person(self, delighted, email):

        delighted.people.create(email=email, send=False)

        response = delighted.people.delete(email=email)

        assert response == {'ok': True}

    def test_delete_person_that_does_not_exist(self, delighted, email):

        response = delighted.people.delete(email=email)

        assert response == {'ok': True}
