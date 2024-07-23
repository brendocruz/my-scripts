from unittest import TestCase
from src.commands.getmidiaresolution import GetMidiaResolution


class TestGetVideoResolution(TestCase):
    infile = './mocks/video.mp4'

    def test_run(self):
        command = GetMidiaResolution(infile=self.infile)
        try:
            command.run()
            command.get_result()
        except:
            self.fail()
