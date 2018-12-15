from django.test import TestCase

from new_dawn_server.modules.client_response import ClientResponse

class ClientResponseTest(TestCase):
    def setUp(self):
        super().setUp()
    
    def test_client_response(self):
        client_response = ClientResponse(success=True, message="Good Request")
        response_dict = client_response.get_response_as_dict()
        self.assertEqual(response_dict["success"], True)
        self.assertEqual(response_dict["message"], "Good Request")