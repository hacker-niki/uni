import unittest
from unittest import mock
from unittest.mock import patch, mock_open
import requests
import os

# Import the function to be tested
from main import download_file  # Make sure 'main' is the correct module name


class TestDownloadFile(unittest.TestCase):

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_file_success(self, mock_open_fn, mock_requests_get, mock_path_exists, mock_makedirs):
        # Mock the response object returned by requests.get
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b'file content'
        mock_requests_get.return_value = mock_response

        # Simulate that the directory already exists
        mock_path_exists.return_value = True

        # Call the function
        url = "http://example.com/file.txt"
        save_dir = "/fake/dir"
        download_file(url, save_dir)

        # Ensure requests.get was called with the URL
        mock_requests_get.assert_called_once_with(url)

        # Ensure open was called correctly to save the file as 'filename'
        file_path = os.path.join(save_dir, 'filename')
        mock_open_fn.assert_called_once_with(file_path, 'wb')

        # Ensure the content was written to the file
        mock_open_fn().write.assert_called_once_with(b'file content')

        # Ensure os.makedirs was not called since the directory exists
        mock_makedirs.assert_not_called()

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_file_directory_creation(self, mock_open_fn, mock_requests_get, mock_path_exists, mock_makedirs):
        # Mock the response object returned by requests.get
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b'some content'
        mock_requests_get.return_value = mock_response

        # Simulate that the directory does not exist
        mock_path_exists.return_value = False

        # Call the function
        url = "http://example.com/anotherfile.txt"
        save_dir = "/another/fake/dir"
        download_file(url, save_dir)

        # Ensure os.makedirs was called to create the directory
        mock_makedirs.assert_called_once_with(save_dir)

        # Ensure open was called correctly to save the file as 'filename'
        file_path = os.path.join(save_dir, 'filename')
        mock_open_fn.assert_called_once_with(file_path, 'wb')

        # Ensure the content was written to the file
        mock_open_fn().write.assert_called_once_with(b'some content')

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('requests.get')
    def test_download_file_http_error(self, mock_requests_get, mock_path_exists, mock_makedirs):
        # Mock an HTTP error response
        mock_requests_get.side_effect = requests.exceptions.HTTPError("HTTP Error")

        # Simulate that the directory exists
        mock_path_exists.return_value = True

        # Use a mock for the print function to capture output
        with patch('builtins.print') as mock_print:
            url = "http://example.com/errorfile.txt"
            save_dir = "/error/fake/dir"
            download_file(url, save_dir)

            # Ensure the error message was printed
            mock_print.assert_called_once_with("Произошла ошибка при загрузке: HTTP Error")

    @patch('os.makedirs')
    @patch('os.path.exists')
    @patch('requests.get')
    def test_download_file_general_exception(self, mock_requests_get, mock_path_exists, mock_makedirs):
        # Mock a general exception during the file write process
        mock_requests_get.side_effect = Exception("General Error")

        # Simulate that the directory exists
        mock_path_exists.return_value = True

        # Use a mock for the print function to capture output
        with patch('builtins.print') as mock_print:
            url = "http://example.com/generalerror.txt"
            save_dir = "/generalerror/fake/dir"
            download_file(url, save_dir)

            # Ensure the error message was printed
            mock_print.assert_called_once_with("Произошла ошибка: General Error")


if __name__ == '__main__':
    unittest.main()
