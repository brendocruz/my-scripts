from unittest import TestCase
import os

from src.commands.cropmidia import CropMidia



class TestCrop(TestCase):
    infile  = './mocks/video.mp4'
    dirtemp = '.temp'
    outfile = '.temp/output.mp4'


    @classmethod
    def setUpClass(cls):
        if not os.path.isdir(cls.dirtemp):
            os.mkdir(cls.dirtemp)


    @classmethod
    def tearDownClass(cls):
        if os.path.isdir(cls.dirtemp):
            os.rmdir(cls.dirtemp)


    def tearDown(self):
        if os.path.isfile(self.outfile):
            os.remove(self.outfile)


    def test_without_size_argument(self):
        with self.assertRaises(ValueError):
            command = CropMidia(self.infile,
                                self.outfile,
                                overwrite=False)
            command.build()


    def test_trbl_boundaries(self):
        tt = 10
        tb = 20
        tl = 200
        tr = 100

        command = CropMidia(self.infile,
                            self.outfile,
                            top=tt,
                            right=tr,
                            bottom=tb,
                            left=tl,
                            overwrite=False)

        try:
            command.build()
        except ValueError:
            self.fail()


    def test_run(self):
        tt = 100
        tr = 100
        tb = 100
        tl = 100

        try:
            CropMidia(self.infile,
                      self.outfile,
                      overwrite=True,
                      top=tt,
                      right=tr,
                      bottom=tb,
                      left=tl).run()
        except:
            self.fail()
