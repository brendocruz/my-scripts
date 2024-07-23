from unittest import TestCase
from unittest.mock import patch
from src.utils.filechecker import file_ouptut_checker
from src.utils.filechecker import file_input_checker


class TestFileOutputChecker(TestCase):
    outfile = 'output.mp4'


    @patch('os.path.isfile')
    def test_exists_as_file_and_overwrite_false(self, mock_isfile):
        mock_isfile.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker(self.outfile, False)


    @patch('os.path.isfile')
    def test_exists_as_file_and_overwrite_true(self, mock_isfile):
        mock_isfile.return_value = True
        try:
            file_ouptut_checker(self.outfile, True)
        except FileExistsError:
            self.fail()


    @patch('os.path.isdir')
    def test_exists_as_directory_and_overwrite_false(self, mock_isdir):
        mock_isdir.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker(self.outfile, False)


    @patch('os.path.isdir')
    def test_exists_as_directory_and_overwrite_true(self, mock_isdir):
        mock_isdir.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker(self.outfile, True)


    @patch('os.path.isdir')
    def test_exists_false(self, mock_isdir):
        mock_isdir.return_value = True
        with self.assertRaises(FileExistsError):
            file_ouptut_checker(self.outfile, True)




class TestFileInputChecker(TestCase):
    infile = 'input.mp4'


    @patch('os.path.isfile')
    def test_exists_true(self, mock_isfile):
        mock_isfile.return_value = True

        try:
            file_input_checker(self.infile)
        except FileNotFoundError:
            self.fail()


    @patch('os.path.isfile')
    def test_exists_false(self, mock_isfile):
        mock_isfile.return_value = False

        with self.assertRaises(FileNotFoundError):
            file_input_checker(self.infile)
