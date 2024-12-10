class InvalidFormatException(Exception):
    """Raised when the format is invalid"""
    pass

class InvalidFileException(Exception):
    """Raised when the file is invalid"""
    pass

class InvalidUrlException(Exception):
    """Raised when the URL is invalid"""
    pass

class DownloadFailedException(Exception):
    """Raised when the download fails"""
    pass

class ConversionFailedException(Exception):
    """Raised when the conversion fails"""
    pass

class FFmpegNotInstalledException(Exception):
    """Raised when FFmpeg is not installed"""
    pass

class PyTgCallsException(Exception):
    """Raised when there is an error in PyTgCalls"""
    pass
