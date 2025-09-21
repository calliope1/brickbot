class BrickBotException(Exception):
    value = 1
    def __init__(self, message):
        self.message = message

class NoChannelException(BrickBotException):
    value = 2
    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.message = f"No channel found with id `{channel_id}`."

class NoMessageException(BrickBotException):
    value = 3
    def __init__(self, message_id, channel_id):
        self.message_id = message_id
        self.channel_id = channel_id
        self.message = f"No message with id `{message_id}` found in channel id `{channel_id}`."

class NonIntIdException(BrickBotException):
    value = 4
    def __init__(self, id_attempt):
        self.id_attempt = id_attempt
        self.message = f"The input id {id_attempt} is not an int."

class TooShortMessageException(BrickBotException):
    value = 5
    def __init__(self, message_content, expected_length):
        self.message_content = message_content
        self.expected_length = expected_length
        self.message = f"Expected {expected_length} characters, only supplied {len(message_content)}: {message_content}."

class UnexpectedLogicPath(BrickBotException):
    value = 6
    def __init__(self):
        self.message = "Unexpected logical path taken. This is a coding error, not a client use error."