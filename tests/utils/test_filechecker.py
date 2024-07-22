from os import walk
from unittest import TestCase
from unittest.mock import patch
from src.utils.filechecker import file_ouptut_checker


class TestFileOutputChecker(TestCase):

    @patch('os.path.isfile')
    def test_exists_as_file_and_overwrite_false(self, mock_isfile):
        mock_isfile.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker('test_file', False)


    @patch('os.path.isfile')
    def test_exists_as_file_and_overwrite_true(self, mock_isfile):
        mock_isfile.return_value = True
        try:
            file_ouptut_checker('test_file', True)
        except FileExistsError:
            self.fail()


    @patch('os.path.isdir')
    def test_exists_as_directory_and_overwrite_false(self, mock_isdir):
        mock_isdir.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker('test_dir', False)


    @patch('os.path.isdir')
    def test_exists_as_directory_and_overwrite_true(self, mock_isdir):
        mock_isdir.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker('test_dir', True)


    @patch('os.path.isdir')
    def test_doesnt_exist(self, mock_isdir):
        mock_isdir.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker('test_dir', True)
