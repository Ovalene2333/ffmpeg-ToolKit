import subprocess
import json
from utils import is_valid_filename, change


class progress:
    def __init__(self):
        self.input_path = ''
        self.output_path = ''
        self.stream_info = []
        self.format_info = {}

    def get_info(self, *args):
        filename = self.input_path
        ffprobe_command = [
            'ffprobe',
            '-v', 'error',
            '-show_format',
            '-show_streams',
            '-of', 'json',
            filename
        ]

        ffprobe_output = subprocess.check_output(ffprobe_command, text=False)

        if ffprobe_output:
            video_info = json.loads(ffprobe_output)
        self.stream_info = video_info['streams']
        self.format_info = video_info['format']

    def Construct(self, filename):
        if not is_valid_filename(filename):
            raise ValueError("Invalid filename")
        self.input_path = filename
        self.get_info()
