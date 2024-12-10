class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)


class UnableToFetchCarbon(Exception):
    pass

class FFmpegNotInstalledException(Exception):
    """Raised when FFmpeg is not installed"""
    pass

class PyTgCallsException(Exception):
    """Raised when there is an error in PyTgCalls"""
    pass
