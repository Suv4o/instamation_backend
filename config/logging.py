import logging

logging.basicConfig(level=logging.DEBUG)


class Logger:
    def __init__(self, name):
        self.name = name

    def get(self):
        return logging.getLogger(self.name)
