
class EndGameException(Exception):
    pass

class GameOverException(EndGameException):
    pass

class LoadStateException(EndGameException):
    def __init__(self, s):
        self.s=s