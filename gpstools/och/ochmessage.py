from datetime import datetime
from .ochutils import OchUtils
from .ochparser import OchParser


class OchMessage:
    def __init__(self, message=None):
        self._full_message = message
        self.latitude = 0
        self.longitude = 0
        self.speed = -1
        self.datetime = None

        if message is not None:
            message = message.replace('\n', ' ').replace('\r', '')
            self._full_message = message
            self._tokens = message.split(OchUtils.Delimiter)
            self.__set_data()

    def __set_data(self):
        self.datetime = self._tokens[0]
        self.latitude = float(self._tokens[1])
        self.longitude = float(self._tokens[2])
        self.speed = float(self._tokens[3])

    def is_valid(self):
        return -90 <= self.latitude <= 90 and -180 <= self.longitude <= 180 and self.speed >= 0 and datetime is not None

    def to_string(self):
        if self._full_message is None:
            return OchUtils.DATA_FORMAT.format(
                OchParser.datetime_to_message(self.datetime), self.latitude, self.longitude, self.speed
            )
        return self._full_message
