from typing import Optional
from dataclasses import dataclass
import subprocess

from src.utils.filechecker import file_ouptut_checker


@dataclass
class GenerateSingleColorImageArgs:
    outfile:   str
    width:     int
    height:    int
    color:     str
    overwrite: Optional[bool] = False



@dataclass
class GenerateSingleColorImage:
    outfile:   str
    width:     int
    height:    int
    color:     str
    overwrite: Optional[bool] = False


    def parse(self) -> GenerateSingleColorImageArgs:
        """Parse the arguments."""
        outfile:    str = self.outfile
        overwrite: bool = False
        width:      int = self.width
        height:     int = self.height
        color:      str = self.color

        if self.overwrite:
            overwrite = True

        file_ouptut_checker(outfile, overwrite)

        return GenerateSingleColorImageArgs(outfile=outfile,
                                            overwrite=overwrite,
                                            width=width,
                                            height=height,
                                            color=color)


    def build(self) -> list[str]:
        """Build the commnad."""
        args = self.parse()

        command = ['ffmpeg',
                   '-f',
                   'lavfi',
                   '-i',
                   f'color={args.color}:{args.width}x{args.height}:d=3,format=rgb24',
                   '-frames:v',
                   '1',
                   '-loglevel',
                   'fatal',
                   args.outfile]

        if args.overwrite:
            command.append('-y')
        else:
            command.append('-n')

        return command


    def run(self) -> None:
        """Run the command."""
        command = self.build()
        subprocess.run(command, cwd='.')
