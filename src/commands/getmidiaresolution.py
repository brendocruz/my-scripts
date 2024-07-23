from typing import NamedTuple
from dataclasses import dataclass, field
import subprocess

from src.utils.filechecker import file_input_checker



class Resolution(NamedTuple):
    width: int
    height: int



@dataclass
class GetMidiaResolutionArgs():
    infile: str



@dataclass
class GetMidiaResolution():
    infile: str
    result: Resolution = field(init=False)


    def parse(self) -> GetMidiaResolutionArgs:
        """Parse the arguments."""
        file_input_checker(self.infile)
        return GetMidiaResolutionArgs(infile=self.infile)


    def build(self) -> list[str]:
        """Build the commnad."""
        args = self.parse()

        command = ['ffprobe',
                   '-loglevel',
                   'error',
                   '-show_entries',
                   'stream=width,height',
                   '-output_format',
                   'csv=p=0',
                   args.infile]
        return command


    def run(self) -> None:
        """Run the command."""
        command = self.build()

        output = subprocess.check_output(command, cwd='.')
        dimensions = output[:-1].decode('utf-8').split(',')

        width = int(dimensions[0])
        height = int(dimensions[1])
        self.result = Resolution(width=width, height=height)


    def get_result(self) -> Resolution:
        """Return the result of the command."""
        return self.result
