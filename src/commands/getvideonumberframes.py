from dataclasses import dataclass, field
import subprocess

from src.utils.filechecker import file_input_checker



@dataclass
class GetVideoNumberOfFramesArgs:
    infile: str



@dataclass
class GetVideoNumberOfFrames:
    infile: str
    result: int = field(init=False)


    def parse(self) -> GetVideoNumberOfFramesArgs:
        """Parse the arguments."""
        file_input_checker(self.infile)
        return GetVideoNumberOfFramesArgs(self.infile)


    def build(self) -> list[str]:
        """Build the command."""
        args = self.parse()

        command = ['ffprobe', 
                   '-select_streams',
                   'v:0', 
                   '-count_packets', 
                   '-show_entries',
                   'stream=nb_read_packets', 
                   '-output_format',
                   'csv=p=0', 
                   '-loglevel', 
                   'error', 
                   args.infile]
        return command


    def run(self) -> None:
        """Run the command."""
        command = self.build()

        output = subprocess.check_output(command, cwd='.')
        frames = int(output[:-1].decode('utf-8'))
        self.result = frames

    
    def get_result(self) -> int:
        """Return the result of the command."""
        return self.result
