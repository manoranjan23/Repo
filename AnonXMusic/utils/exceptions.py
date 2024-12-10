class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)


class UnableToFetchCarbon(Exception):
    pass

import subprocess

class FFmpegNotInstalledException(Exception):
    """Raised when FFmpeg is not installed"""
    pass

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], check=True)
    except FileNotFoundError:
        raise FFmpegNotInstalledException("FFmpeg is not installed")

try:
    check_ffmpeg()
except FFmpegNotInstalledException as e:
    print(e)
