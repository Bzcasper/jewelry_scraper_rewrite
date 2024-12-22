# tests/backend/test_auth.py

import unittest
from unittest.mock import MagicMock, patch
from backend.auth.routes import register, login
from backend.database.manager import DatabaseManager

class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        self.db_manager = MagicMock(spec=DatabaseManager)

    @patch('backend.auth.routes.db_manager', new_callable=MagicMock)
    def test_register_success(self, mock_db_manager):
        mock_db_manager.add_user.return_value = None
        with patch('flask.request') as mock_request:
            mock_request.get_json.return_value = {
                'username': 'testuser',
                'password': 'testpass',
                'role': 'admin'
            }
            response = register()
            self.assertEqual(response[1], 201)
            mock_db_manager.add_user.assert_called_once()

    @patch('backend.auth.routes.db_manager', new_callable=MagicMock)
    def test_login_success(self, mock_db_manager):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.password = 'hashedpass'
        mock_db_manager.get_user_by_username.return_value = mock_user

        with patch('flask.request') as mock_request, \
             patch('werkzeug.security.check_password_hash', return_value=True), \
             patch('jwt.encode', return_value='fake_token'):

            mock_request.get_json.return_value = {
                'username': 'testuser',
                'password': 'testpass'
            }
            response = login()
            self.assertEqual(response[1], 200)
            self.assertIn('token', response[0].json)

    @patch('backend.auth.routes.db_manager', new_callable=MagicMock)
    def test_login_failure_wrong_credentials(self, mock_db_manager):
        mock_db_manager.get_user_by_username.return_value = None

        with patch('flask.request') as mock_request:
            mock_request.get_json.return_value = {
                'username': 'nonexistent',
                'password': 'nopass'
            }
            response = login()
            self.assertEqual(response[1], 401)
            self.assertIn('User not found', response[0].json['message'])

if __name__ == '__main__':
    unittest.main()
