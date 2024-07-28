from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
import subprocess
import os

from src.commands.getvideonumberframes import GetVideoNumberOfFrames
from src.commands.getvideoduration import GetVideoDuration

from src.utils.filechecker import file_input_checker
from src.utils.filechecker import file_output_checker


@dataclass
class ExtractVideosFramesArgs():
    infile:    str
    outfile:   str
    frames:    Optional[list[int]] = None
    start:     Optional[str]       = None
    end:       Optional[str]       = None
    all:       bool                = False
    overwrite: bool                = False



@dataclass
class ExtractVideoFrames():
    infile:    str
    outfile:   Optional[str]             = None
    destdir:   Optional[str]             = None
    frames:    Optional[int | list[int]] = None
    start:     Optional[timedelta]       = None
    end:       Optional[timedelta]       = None
    duration:  Optional[timedelta]       = None
    all:       Optional[bool]            = False
    overwrite: Optional[bool]            = False


    def parse(self):
        infile     = self.infile
        outfile    = self.outfile
        destdir    = self.destdir
        frames:    Optional[int | list[int]]  = None
        start:     Optional[str]              = None
        end:       Optional[str]              = None
        all:       bool                       = bool(self.all)
        overwrite: bool                       = bool(self.overwrite)


        file_input_checker(infile)


        if self.frames and type(self.frames) is int:
            frames = [self.frames]
        if self.frames and type(self.frames) is list:
            frames = self.frames

        
        if frames:
            command = GetVideoNumberOfFrames(self.infile)
            command.run()
            total_frames = command.get_result()

            filtered = list(filter(lambda x: x <= 0, frames))
            if len(filtered) > 0:
                raise ValueError(f'Frame number(s) should be greater than `0`.')

            filtered = list(filter(lambda x: x > total_frames, frames))
            if len(filtered) > 0:
                raise ValueError(f'Frame number(s) given too high. '
                                 f'Only `{total_frames}` were counted')

            # # In ffmpeg, frames start at zero, so `-1` is needed.
            frames = list(map(lambda x: x - 1, frames))

        

        if self.start and self.end:
            command = GetVideoDuration(self.infile)
            command.run()
            duration = command.get_result()

            if self.start > duration:
                raise ValueError('Start time should be less than duration time'
                                 f'(`{self.start}` < `{self.duration}`).')
            if self.end > duration:
                raise ValueError('End time should be less than duration time '
                                 f'(`{self.end}` < `{self.duration}`).')
            if self.start > self.end:
                raise ValueError('Start time should be less than end time '
                                 f'(`{self.start}` < `{self.end}`).')

            start = str(self.start)
            end = str(self.end)


        if self.start and self.duration:
            command = GetVideoDuration(self.infile)
            command.run()
            duration = command.get_result()

            if self.start > duration:
                raise ValueError('Start time should be less than duration time'
                                 f'(`{self.start}` < `{self.duration}`).')

            if self.start + self.duration > duration:
                raise ValueError('End time should be less than duration time'
                                 f'(`{self.start}` + `{self.duration}` ' 
                                 f'= {self.start + self.duration} < '
                                 f'`{self.duration}`).')

            start = str(self.start)
            end = str(self.start + self.duration)


        if not frames and not start and not end and not all:
            raise ValueError('Missing arguments.')


        inroot, _ = os.path.splitext(os.path.basename(infile))
        if frames and len(frames) == 1 and not outfile:
            outfile = f'{inroot}.png'
        elif not outfile:
            outfile = f'{inroot}-%d.png'
            if not destdir:
                destdir = f'{inroot}'

        if not destdir:
            destdir = ''


        outdir  = os.path.dirname(outfile)
        outname = os.path.basename(outfile)
        fulldir = os.path.join(destdir, outdir)
        if fulldir:
            if not frames or frames is list and len(frames) > 1:
                file_output_checker(fulldir)
            os.makedirs(fulldir, exist_ok=True)


        fullpath = os.path.join(fulldir, outname)
        file_output_checker(fullpath, overwrite)

        return ExtractVideosFramesArgs(infile=infile,
                                       outfile=fullpath,
                                       frames=frames,
                                       start=start,
                                       end=end,
                                       all=all,
                                       overwrite=overwrite)



    def build(self) -> list[str]:
        args = self.parse()

        command = ['ffmpeg',
                   '-i', 
                   args.infile]

        if args.frames:
            frames = '+'.join(map(lambda x: f'eq(n\\,{x})', args.frames))
            command.extend(['-filter:v',
                            f'select={frames}'])

        if args.start and args.end:
            command.extend(['-ss',
                            args.start, 
                            '-to', 
                            args.end])

        command.extend(['-vsync', '0'])
        command.append(args.outfile)


        command.extend(['-loglevel',
                        'error'])


        if args.overwrite:
            command.append('-y')
        else:
            command.append('-n')

        return command



    def run(self) -> None:
        command = self.build()
        subprocess.run(command, cwd='.')

