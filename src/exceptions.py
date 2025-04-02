class ImageError(Exception):
    """Custom exception for errors returned by Amazon Nova Canvas"""

    def __init__(self, message):
        self.message = message 