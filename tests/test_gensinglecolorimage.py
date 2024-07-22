from unittest import TestCase
import os

from src.commands.gensinglecolorimage import GenerateSingleColorImage


class TestGenerateImageSolid(TestCase):
    dir_temp = '.temp'
    outfile = '.temp/image.png'
    width = 640
    height = 480
    color = 'red'


    def setUp(self):
        if not os.path.isdir(self.dir_temp):
            os.mkdir(self.dir_temp)


    def test_overwrite(self):
        # (1) For `overwrite = False`.
        command = GenerateSingleColorImage(outfile=self.outfile,
                                           overwrite=False,
                                           width=self.width,
                                           height=self.height,
                                           color=self.color)
        command.run()

        with self.assertRaises(FileExistsError):
            command.run()


        # (2) For `overwrite = True`.
        command.overwrite = True
        try:
            command.run()
        except:
            self.fail()


    def tearDown(self):
        os.remove(self.outfile)
        os.rmdir(self.dir_temp)
