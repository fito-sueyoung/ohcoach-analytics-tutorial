from datetime import datetime


class NmeaParser:

    @staticmethod
    def message_to_latitude_decimal(msg_latitude_dms, n_or_s):
        degree = int(msg_latitude_dms[0:(msg_latitude_dms.index('.') - 2)])
        minute = float(msg_latitude_dms[(msg_latitude_dms.index('.') - 2):])

        latitude = degree + minute / 60.0
        if n_or_s == 'S':
            latitude = - latitude
        return latitude

    @staticmethod
    def message_to_longitude_decimal(msg_longitude_dms, e_or_w):
        degree = int(msg_longitude_dms[0:(msg_longitude_dms.index('.') - 2)])
        minute = float(msg_longitude_dms[(msg_longitude_dms.index('.') - 2):])

        longitude = degree + minute / 60.0
        if e_or_w == 'W':
            longitude = - longitude
        return longitude

    @staticmethod
    def message_to_speed_kilos(msg_speed_knots):
        return float(msg_speed_knots) * 1.852

    @staticmethod
    def message_to_datetime(utc_datestamp, utc_timestamp):
        dt_str = f'{utc_datestamp[:4]}20{utc_datestamp[4:6]} {utc_timestamp}'
        return datetime.strptime(dt_str, '%d%m%Y %H%M%S.%f')

    @staticmethod
    def datetime_to_message(dt):
        utc_date_stamp = dt.strftime('%d%m%Y')
        utc_time_stamp = dt.strftime('%H%M%S.%f')
        utc_time_stamp = utc_time_stamp[:utc_time_stamp.index('.')+3]
        return [utc_date_stamp, utc_time_stamp]

    @staticmethod
    def message_to_checksum(full_message):
        check_msg = full_message[full_message.find('$') + 1:full_message.find('*')]
        checksum = 0
        for i in range(len(check_msg)):
            checksum = checksum ^ ord(check_msg[i])
        return checksum
