from unittest import TestCase
from src.commands.getvideoduration import GetVideoDuration


class TestGetVideoResolution(TestCase):
    infile = './mocks/video.mp4'

    def test_run(self):
        command = GetVideoDuration(infile=self.infile)
        try:
            command.run()
            command.get_result()
        except:
            self.fail()
