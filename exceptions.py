class EmptyQueryException(Exception):
    """An exception class for cases where user query is empty."""
 
    def __init__(self, message=None):
        self.message = message
