from unittest import TestCase
from unittest.mock import patch
from datetime import timedelta
from shutil import rmtree
import os

from src.commands.extractframes import ExtractVideoFrames



class TestExtractVideoFrameCommand(TestCase):
    infile  = './mocks/video.mp4'
    outfile = 'output.png'
    subdir  = 'output-video'
    destdir = '.temp-314159'



    def setUp(self):
        path = os.path.join(os.getcwd(), self.destdir)
        if path == '':
            return

        if os.path.isdir(path):
            rmtree(path)



    def tearDown(self):
        path = os.path.join(os.getcwd(), self.destdir)
        if path == '':
            return

        if os.path.isdir(path):
            rmtree(path)



    def test_frames_with_int(self):
        frame   = 14
        command = ExtractVideoFrames(infile=self.infile,
                                     outfile=self.outfile,
                                     frames=frame,
                                     overwrite=True)
        args = command.parse()
        if type(args.frames) is not list:
            self.fail()
        self.assertListEqual(args.frames, [frame - 1])



    def test_frames_with_int_and_outfile(self):
        command = ExtractVideoFrames(infile=self.infile,
                                     outfile=self.outfile,
                                     frames=1)

        args = command.parse()
        self.assertEqual(self.outfile, args.outfile)



    def test_frames_with_int_and_no_outfile(self):
        command = ExtractVideoFrames(infile=self.infile,
                                     frames=1)

        args = command.parse()
        self.assertEqual('video.png', args.outfile)



    def test_frames_with_list_and_negatives(self):
        frames  = [5, 10, 15, -20, 25, 30]
        command = ExtractVideoFrames(infile=self.infile,
                                     outfile=self.outfile,
                                     frames=frames,
                                     overwrite=True)

        with self.assertRaises(ValueError):
            command.build()



    def test_frames_with_list_and_high_number(self):
        frame   = [5, 10, 15, 31415926535897, 25, 30]
        command = ExtractVideoFrames(infile=self.infile,
                                     outfile=self.outfile,
                                     frames=frame,
                                     overwrite=True)

        with self.assertRaises(ValueError):
            command.build()



    def test_start_with_end_valid(self):
        start   = timedelta(minutes=0, seconds=5)
        end     = timedelta(minutes=0, seconds=10)
        command = ExtractVideoFrames(infile=self.infile,
                                     outfile=self.outfile,
                                     start=start,
                                     end=end)
        args = command.parse()
        self.assertEqual(args.start, str(start))
        self.assertEqual(args.end, str(end))



    def test_start_with_end_invalid_start(self):
        start   = timedelta(minutes=35, seconds=10)
        end     = timedelta(minutes=0,  seconds=10)
        command = ExtractVideoFrames(infile=self.infile, 
                                     outfile=self.outfile,
                                     start=start, 
                                     end=end)

        with self.assertRaises(ValueError):
            command.parse()



    def test_start_with_end_invalid_end(self):
        start   = timedelta(minutes=0,  seconds=5)
        end     = timedelta(minutes=35, seconds=10)
        command = ExtractVideoFrames(infile=self.infile, 
                                     outfile=self.outfile,
                                     start=start, 
                                     end=end)

        with self.assertRaises(ValueError):
            command.parse()



    def test_start_with_end_start_greater(self):
        start   = timedelta(minutes=0, seconds=10)
        end     = timedelta(minutes=0, seconds=5)
        command = ExtractVideoFrames(infile=self.infile, 
                                     outfile=self.outfile,
                                     start=start, 
                                     end=end)

        with self.assertRaises(ValueError):
            command.parse()



    def test_start_with_duration_valid(self):
        start    = timedelta(minutes=0, seconds=5)
        duration = timedelta(minutes=0, seconds=10)
        command  = ExtractVideoFrames(infile=self.infile,
                                      outfile=self.outfile,
                                      start=start,
                                      duration=duration)

        args = command.parse()
        self.assertEqual(args.start, str(start))
        self.assertEqual(args.end, str(start + duration))



    def test_start_with_duration_invalid_start(self):
        start    = timedelta(minutes=35, seconds=10)
        duration = timedelta(minutes=0,  seconds=5)
        command  = ExtractVideoFrames(infile=self.infile, 
                                      outfile=self.outfile,
                                      start=start, 
                                      duration=duration)

        with self.assertRaises(ValueError):
            command.parse()



    def test_start_with_duration_invalid_duration(self):
        start    = timedelta(minutes=0,  seconds=5)
        duration = timedelta(minutes=35, seconds=10)
        command  = ExtractVideoFrames(infile=self.infile, 
                                      outfile=self.outfile,
                                      start=start, 
                                      duration=duration)

        with self.assertRaises(ValueError):
            command.parse()



    def test_specify_no_frame_to_extract(self):
        command = ExtractVideoFrames(infile=self.infile, 
                                     outfile=self.outfile)

        with self.assertRaises(ValueError):
            command.parse()



    @patch('os.makedirs')
    def test_frames_with_list_and_no_output(self, mock_makedirs):
        mock_makedirs.return_value = None

        frames  = [10, 20, 30, 40, 50]
        command = ExtractVideoFrames(infile=self.infile,
                                     frames=frames)

        args = command.parse()
        self.assertEqual('video/video-%d.png', args.outfile)



    def test_run_with_frames(self):
        frames = [10, 20, 30]
        command = ExtractVideoFrames(infile=self.infile,
                                     destdir=self.destdir,
                                     frames=frames)

        try:
            command.run()
        except:
            self.fail()



    def test_run_with_frames_and_overwrite(self):
        frames = 10
        command = ExtractVideoFrames(infile=self.infile,
                                     destdir=self.destdir,
                                     frames=frames,
                                     overwrite=True)

        try:
            command.run()
        except:
            self.fail()



    def test_run_with_start_end(self):
        start   = timedelta(seconds=5)
        end     = timedelta(seconds=10)
        destdir = os.path.join(self.destdir, self.subdir)
        command = ExtractVideoFrames(infile=self.infile,
                                     start=start,
                                     end=end,
                                     destdir=destdir)

        try:
            command.run()
        except:
            self.fail()



    def test_run_with_start_duration(self):
        start    = timedelta(seconds=5)
        duration = timedelta(seconds=10)
        destdir  = os.path.join(self.destdir, self.subdir)
        command  = ExtractVideoFrames(infile=self.infile,
                                      start=start,
                                      duration=duration,
                                      destdir=destdir)

        try:
            command.run()
        except:
            self.fail()
