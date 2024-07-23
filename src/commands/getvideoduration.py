from datetime import timedelta, datetime
from dataclasses import dataclass, field
import subprocess

from src.utils.filechecker import file_input_checker



@dataclass
class GetVideoDurationArgs:
    infile: str



@dataclass
class GetVideoDuration:
    infile: str
    result: timedelta = field(init=False)


    def parse(self):
        """Parse the arguments."""
        file_input_checker(self.infile)
        return GetVideoDurationArgs(self.infile)


    def build(self) -> list[str]:
        """Build the command."""
        args = self.parse()
        command = ['ffprobe', 
                   '-show_entries', 
                   'format=duration',
                   '-output_format', 
                   'default=noprint_wrappers=1:nokey=1', 
                   '-sexagesimal',
                   '-loglevel', 
                   'error', 
                   args.infile]
        return command


    def run(self) -> None:
        """Run the command."""
        command = self.build()

        output = subprocess.check_output(command, cwd='.')

        duration = output[:-1].decode('utf-8')
        dt = datetime.strptime(duration, '%H:%M:%S.%f')
        delta = timedelta(hours=dt.hour,
                          minutes=dt.minute,
                          seconds=dt.second,
                          microseconds=dt.microsecond)
        self.result = delta


    def get_result(self) -> timedelta:
        """Return the result of the command."""
        return self.result
