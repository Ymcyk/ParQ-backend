from django.test import TestCase
from django.contrib.auth.models import Group, User
from djroles.models import Role

from .models import Driver, Officer

class UsersTest(TestCase):

    def setUp(self):
        self.officer_group = Role.objects.create_role(name='Officer')
        self.driver_group = Role.objects.create_role(name='Driver')

    def test_officer_is_created(self):
        # prepare
        officer = Officer.objects.create_user(username='test_user')
        # do
        group = Role.objects.get_user_role(officer)
        # check
        self.assertTrue(group == self.officer_group, 
                msg='Officer with bad group')

    def test_driver_is_created(self):
        # prepare
        user = User.objects.create_user(username='Jan')
        driver = Driver.objects.create(user=user)
        # do
        group = Role.objects.get_user_role(user)
        # check
        self.assertTrue(group == self.driver_group, msg='Bad group')

from .serializers import DriverSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO

class DriverSerializationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Piotr', email='ziel135@o2.pl')
        self.driver_group = Role.objects.create_role(name='Driver')
        self.driver = Driver.objects.create(user=self.user)

    def serialize(self):
        self.serializer = DriverSerializer(self.driver)
        self.content = JSONRenderer().render(self.serializer.data)

    def test_test(self):
        self.serialize()
        print('JSON:', self.content)

    def test_create(self):
        content = b'{"user":{"username":"Adam","email":"ziel135@o2.pl"},"wallet":"0.00"}'
        stream = BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = DriverSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg='Data not valid')
        serializer.save()
        self.assertEqual(len(Driver.objects.all()), 2)
