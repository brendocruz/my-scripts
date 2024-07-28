from dataclasses import dataclass
from typing import Optional
import subprocess

from src.utils.filechecker import file_input_checker
from src.utils.filechecker import file_output_checker



@dataclass
class CropMidiaArgs:
    infile:    str
    outfile:   str
    x:         int
    y:         int
    width:     int | str
    height:    int | str
    overwrite: bool



@dataclass
class CropMidia():
    infile:    str
    outfile:   str
    x:         Optional[int]  = None
    y:         Optional[int]  = None
    width:     Optional[int]  = None
    height:    Optional[int]  = None
    top:       Optional[int]  = None
    bottom:    Optional[int]  = None
    left:      Optional[int]  = None
    right:     Optional[int]  = None
    overwrite: Optional[bool] = None


    def parse(self) -> CropMidiaArgs:
        infile    = self.infile
        outfile   = self.outfile
        overwrite = False

        if self.overwrite:
            overwrite = True

        file_input_checker(infile)
        file_output_checker(outfile)

        x      = self.x
        y      = self.y
        width  = self.width
        height = self.height

        if self.right and self.left and self.top and self.bottom:
            x = self.top
            y = self.left
            width  = f'iw-{self.left + self.right}'
            height = f'ih-{self.top + self.bottom}'

        if not x or not y or not width or not height:
            raise ValueError('Invalid arguments')

        return CropMidiaArgs(infile=infile,
                             outfile=outfile,
                             x=x,
                             y=y,
                             width=width,
                             height=height,
                             overwrite=overwrite)


    def build(self) -> list[str]:
        args = self.parse()

        command = ['ffmpeg',
                   '-i',
                   args.infile,
                   '-filter:v',
                   f'crop={args.width}:{args.height}:{args.x}:{args.y}',
                   '-loglevel',
                   'error',
                   args.outfile]

        if args.overwrite:
            command.append('-y')
        else:
            command.append('-n')
        return command


    def run(self) -> None:
        command = self.build()
        subprocess.run(command, cwd='.')
