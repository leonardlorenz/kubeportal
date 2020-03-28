from django.contrib.auth.hashers import make_password
from django.test import TestCase, client
from django.contrib.auth import get_user_model
from kubeportal import models

admin_clear_password = 'adminäö&%/1`'

admin_data = {
    'username': 'adminäö&%/1`',
    'email': 'adminäö&%/1`@example.com',
    'password': make_password(admin_clear_password),
    'is_staff': True,
    'is_superuser': True
}


class BaseTestCase(TestCase):
    def setUp(self):
        self.c = client.Client()

class AnonymousTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

class AdminLoggedOutTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        User = get_user_model()
        self.admin = User(**admin_data)
        self.admin.save()
        self.admin_group = models.PortalGroup(name="Admins", auto_admin=True)
        self.admin_group.save()
        self.admin_group.members.add(self.admin)
        self.admin_group.save()

class AdminLoggedInTestCase(AdminLoggedOutTestCase):
    def login_admin(self):
        self.c.login(username=admin_data['username'],
                     password=admin_clear_password)

    def setUp(self):
        super().setUp()
        self.login_admin()


