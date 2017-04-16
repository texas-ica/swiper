class ParseError(Exception):
    def __init__(self, message):
        self.message = message
        super(ParseException, self).__init__(message)
