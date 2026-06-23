# custom exceptions 
class InvalidAPIKeyException(Exception):
    def __init__(self):
        self.message = "Invalid or missing API key"