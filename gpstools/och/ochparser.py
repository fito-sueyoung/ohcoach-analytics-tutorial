from datetime import datetime
from .ochutils import OchUtils


class OchParser:

    @staticmethod
    def message_to_latitude_nmea(msg_latitude):
        latitude = float(msg_latitude)

        if latitude >= 0:
            n_or_s = 'N'
        else:
            n_or_s = 'S'

        degree = int(latitude)
        minute = (latitude-degree) * 60
        msg_latitude_dms = "{:.5f}".format(degree*100+minute)

        return [msg_latitude_dms, n_or_s]

    @staticmethod
    def message_to_longitude_nmea(msg_longitude):
        longitude = float(msg_longitude)

        if longitude >= 0:
            e_or_w = 'E'
        else:
            e_or_w = 'W'

        degree = int(longitude)
        minute = (longitude-degree) * 60
        msg_longitude_dms = "{:.5f}".format(degree*100+minute)

        return [msg_longitude_dms, e_or_w]

    @staticmethod
    def message_to_speed_knots(msg_speed_killos):
        return float(msg_speed_killos) / 1.852

    @staticmethod
    def message_to_datetime(datetime_stamp):
        tokens = datetime_stamp.split('.')
        year = int(tokens[0])
        month = int(tokens[1])
        date = int(tokens[2])
        hour = int(tokens[3])
        minute = int(tokens[4])
        second = int(tokens[5])
        millisecond = int(tokens[6]) * 100

        dt = datetime(year, month, date, hour, minute, second, millisecond * 1000)
        return dt

    @staticmethod
    def datetime_to_message(dt):
        return dt.strftime(OchUtils.DATETIME_FORMAT)[:-5]
