import unittest
from unittest.mock import patch, MagicMock
import os
from src.email_service import send_epub_email

class TestEmailService(unittest.TestCase):

    @patch('src.email_service.smtplib.SMTP')
    @patch('src.email_service.get_config')
    @patch('src.email_service.os.getenv')
    @patch('src.email_service.os.path.exists')
    @patch('builtins.open', new_callable=MagicMock)
    def test_send_epub_email_success(self, mock_open, mock_exists, mock_getenv, mock_get_config, mock_smtp):
        # Setup mocks
        mock_get_config.return_value = {"enabled": True, "subject": "Test {title}", "body": "Body {title}"}
        mock_exists.return_value = True

        # Mock file reading
        mock_file = MagicMock()
        mock_file.read.return_value = b"fake pdf content"
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock Environment variables
        env_vars = {
            "SMTP_SERVER": "smtp.test.com",
            "SMTP_PORT": "587",
            "SMTP_USERNAME": "user",
            "SMTP_PASSWORD": "password",
            "EMAIL_SENDER": "sender@test.com",
            "EMAIL_RECIPIENT": "recipient@test.com"
        }
        mock_getenv.side_effect = lambda k: env_vars.get(k)

        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call function
        result = send_epub_email("path/to/book.epub", "My Book")

        # Assertions
        self.assertTrue(result)
        mock_smtp.assert_called_with("smtp.test.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with("user", "password")
        mock_server.send_message.assert_called_once()

    @patch('src.email_service.get_config')
    def test_send_epub_email_disabled(self, mock_get_config):
        mock_get_config.return_value = {"enabled": False}
        result = send_epub_email("path/to.epub", "Title")
        self.assertFalse(result)

    @patch('src.email_service.get_config')
    @patch('src.email_service.os.getenv')
    def test_send_epub_email_missing_env(self, mock_getenv, mock_get_config):
        mock_get_config.return_value = {"enabled": True}
        mock_getenv.return_value = None # All env vars missing
        result = send_epub_email("path/to.epub", "Title")
        self.assertFalse(result)
