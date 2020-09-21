import pytz
import pandas as pd
from io import StringIO
from gpstools.nmea.nmeaparser import NmeaParser
from gpstools.nmea.nmeamessage import NmeaRmcMessage
from gpstools.och.ochutils import OchUtils
from gpstools.och.ochmessage import OchMessage
from gpstools.och.ochparser import OchParser


class OchToGpConverter:
    def __init__(self):
        self.__nmeaMessageList = []
        self.__gp_df = None

    def convert(self, och_data):
        """
        :param och_data: String body of och file
        :return: The dataframe of gp, converted from the och data
        """
        content_lines = och_data.splitlines()[1:]
        self.__nmeaMessageList.clear()

        for str_line in content_lines:
            try:
                if not OchUtils.is_och_format(str_line):  # TODO: takes long time?
                    continue

                och_message = OchMessage(str_line)
                nmea_message = OchToGpConverter.__parse_och_message_to_nmea_message(och_message)

                if nmea_message is not None:
                    self.__nmeaMessageList.append(nmea_message)
            except (ValueError, IndexError):
                pass

        # Convert to dataframe
        gp_csv_str = '\r\n'.join([line.to_string() for line in self.__nmeaMessageList])
        self.__gp_df = pd.read_csv(StringIO(gp_csv_str), sep=',', header=None, dtype=NmeaRmcMessage.DATA_DTYPES)
        return self.__gp_df

    def generate_gp_file(self, target_filepath):
        self.__gp_df.to_csv(target_filepath, index=False, header=None, float_format='%.3f')

    @staticmethod
    def __parse_och_message_to_nmea_message(och_message):
        if och_message is None or not och_message.is_valid():
            return None

        # TODO : only RMC message still..
        nmea_message = NmeaRmcMessage()
        # latitude
        latitude_dms = OchParser.message_to_latitude_nmea(och_message.latitude)
        nmea_message.latitude_dms = latitude_dms[0]
        nmea_message.north_or_south = latitude_dms[1]
        # longitude
        longitude_dms = OchParser.message_to_longitude_nmea(och_message.longitude)
        nmea_message.longitude_dms = longitude_dms[0]
        nmea_message.east_or_west = longitude_dms[1]
        # speed
        nmea_message.speed_knot = OchParser.message_to_speed_knots(och_message.speed)
        # datetime
        local_datetime = OchParser.message_to_datetime(och_message.datetime)
        local_tz = pytz.timezone('Asia/Seoul')
        local_datetime = local_tz.localize(local_datetime, is_dst=None)
        utc_datetime = local_datetime.astimezone(pytz.utc)
        utc_datetime_stamps = NmeaParser.datetime_to_message(utc_datetime)
        nmea_message.datetime = utc_datetime
        nmea_message.utc_datestamp = utc_datetime_stamps[0]
        nmea_message.utc_timestamp = utc_datetime_stamps[1]
        nmea_message.checksum = NmeaParser.message_to_checksum(nmea_message.to_string())

        if nmea_message is not None and nmea_message.is_valid():
            return nmea_message
        else:
            return None



