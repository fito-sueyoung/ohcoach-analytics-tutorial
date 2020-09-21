import pandas as pd
import pytz
from timezonefinder import TimezoneFinder

from gpstools.och.ochutils import OchUtils
from gpstools.nmea.nmeautils import NmeaUtils
from gpstools.nmea.nmeamessage import NmeaMessage, NmeaRmcMessage
from gpstools.nmea.nmeaparser import NmeaParser
from gpstools.och.ochmessage import OchMessage


class GpToOchConverter:
    def __init__(self):
        self.__och_df = None

    def convert(self, gp_data):
        """
        :param gp_data: String body of gp file with NMEA format
        :return: The dataframe of och (och_df), converted from the gp data
        """
        content_lines = gp_data.splitlines()
        och_list = []
        for str_line in content_lines:
            try:
                och_message = self.__parse_nmea_message_to_och_message(str_line)
                if och_message is not None and och_message.is_valid():
                    och_list += [[och_message.datetime, och_message.latitude,
                                  och_message.longitude, och_message.speed]]
            except (ValueError, IndexError):
                pass

        # Convert och_list to DataFrame
        self.__och_df = pd.DataFrame(och_list, columns=OchUtils.HEADER_OCH)

        # Find timezone using geographic coordinates and convert datetime w.r.t. the timezone
        lat, long = self.__och_df[[OchUtils.LABEL_LATITUDE, OchUtils.LABEL_LONGITUDE]].mean()
        tz = pytz.timezone(TimezoneFinder().timezone_at(lat=lat, lng=long))
        start_dt = self.__och_df.at[0, OchUtils.LABEL_DATETIME]
        self.__och_df[OchUtils.LABEL_DATETIME] = self.__och_df[OchUtils.LABEL_DATETIME] + tz.utcoffset(start_dt)
        return self.__och_df

    @staticmethod
    def __parse_nmea_message_to_och_message(str_line):
        if not NmeaUtils.is_nmea_format(str_line):
            return None

        nmea_message_type = NmeaMessage.get_message_type(str_line)
        if nmea_message_type == NmeaUtils.MessageType.RMC:
            nmea_message = NmeaRmcMessage(str_line)
        else:
            nmea_message = None

        if nmea_message is None or not nmea_message.is_valid():
            return None

        och_message = OchMessage()
        if nmea_message.message_code in NmeaUtils.MessageType.RMC:
            och_message.latitude = NmeaParser.message_to_latitude_decimal(
                nmea_message.latitude_dms, nmea_message.north_or_south)
            och_message.longitude = NmeaParser.message_to_longitude_decimal(
                nmea_message.longitude_dms, nmea_message.east_or_west)
            och_message.speed = NmeaParser.message_to_speed_kilos(nmea_message.speed_knot)
            och_message.datetime = NmeaParser.message_to_datetime(
                nmea_message.utc_datestamp, nmea_message.utc_timestamp)
        return och_message
