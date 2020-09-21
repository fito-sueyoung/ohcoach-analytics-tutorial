from abc import abstractmethod
from gpstools.nmea.nmeautils import NmeaUtils


class NmeaMessage:
    def __init__(self, message=None):
        self._full_message = message
        if message is not None:
            message = message.replace('\n', ' ').replace('\r', '')
            self._tokens = message.split(NmeaUtils.Delimiter)
            self._message_type = self._tokens[0][3:6]

    @staticmethod
    def get_message_type(message):
        return message[:message.index(',')][3:6]

    @abstractmethod
    def __set_data(self):
        pass

    @abstractmethod
    def is_valid(self):
        return self._tokens[0] is not None and self._tokens[0][0] == '$'

    def to_string(self):
        if self._full_message is None:
            pass
        else:
            return self._full_message

    @property
    def message_code(self):
        return self._message_type


class NmeaRmcMessage(NmeaMessage):
    DATA_FORMAT = "$GN{},{},A,{},{},{},{},{:.3f},,{},,,A*{:02X}"
    DATA_DTYPES = {0: str, 1: str, 2: str, 3: str, 4: str, 5: str, 6: str,
                   7: float, 8: str, 9: str, 10: str, 11: str, 12: str}

    def __init__(self, message=None):
        NmeaMessage.__init__(self, message)
        self._message_type = NmeaUtils.MessageType.RMC
        self.datetime = []
        self.utc_datestamp = []
        self.utc_timestamp = []
        self.latitude_dms = []
        self.north_or_south = ''    # north=N, south=S for latitude
        self.longitude_dms = []
        self.east_or_west = ''      # east=E, west=W for longitude
        self.speed_knot = -1
        self.active_or_void = 'A'   # active=A, void=V
        self.checksum = -1
        if message is not None:
            self.__set_data()

    def __set_data(self):
        self.utc_timestamp = self._tokens[1]
        self.active_or_void = self._tokens[2]
        self.latitude_dms = self._tokens[3]
        self.north_or_south = self._tokens[4]
        self.longitude_dms = self._tokens[5]
        self.east_or_west = self._tokens[6]
        self.speed_knot = self._tokens[7]
        self.utc_datestamp = self._tokens[9]
        self.checksum = self._tokens[12][:2]

    def is_valid(self):
        return super(NmeaRmcMessage, self).is_valid and \
               self.message_code == NmeaUtils.MessageType.RMC and self.active_or_void == 'A'

    def to_string(self):
        if self._full_message is None:
            return NmeaRmcMessage.DATA_FORMAT.format(
                self.message_code, self.utc_timestamp,
                self.latitude_dms, self.north_or_south, self.longitude_dms, self.east_or_west,
                self.speed_knot, self.utc_datestamp, self.checksum
            )
        return self._full_message

    @property
    def message_code(self):
        return self._message_type
