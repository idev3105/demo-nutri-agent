import unittest
from flask import Flask
from main import app  # Import the Flask app from your main.py
import io

class TestRunAgentAPI(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def test_run_agent_with_image(self):
        # Simulate sending an image file to the API
        with open("test.png", "rb") as test_image:
            data = {
                'image': (io.BytesIO(test_image.read()), 'test.png')
            }
            response = self.app.post('/run_agent', content_type='multipart/form-data', data=data)

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        print(response.json)

if __name__ == '__main__':
    unittest.main()