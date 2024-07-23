from unittest import TestCase
from src.commands.getvideonumberframes import GetVideoNumberOfFrames


class TestGetVideoResolution(TestCase):
    infile = './mocks/video.mp4'

    def test_run(self):
        command = GetVideoNumberOfFrames(infile=self.infile)
        try:
            command.run()
            command.get_result()
        except:
            self.fail()