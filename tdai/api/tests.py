from django.test import TestCase
from api.services import service_variable

# Create your tests here.
class ServiceVariableTestCase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_check_variable_type(self):
        rs = service_variable.check_variable_type('Xin chào', variable_type='String')
        self.assertEqual(rs, True)