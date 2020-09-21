class OchUtils:
    LABEL_DATETIME = 'datetime'
    LABEL_LATITUDE = 'latitude'
    LABEL_LONGITUDE = 'longitude'
    LABEL_SPEED = 'speed'
    HEADER_OCH = [LABEL_DATETIME, LABEL_LATITUDE, LABEL_LONGITUDE, LABEL_SPEED]

    Delimiter = ','
    DATETIME_FORMAT = '%Y.%m.%d.%H.%M.%S.%f'
    DATA_FORMAT = "{},{},{},{:.6f}"

    class MessageType:
        AAM = 'AAM'
        ALM = 'ALM'
        APA = 'APA'
        APB = 'APB'
        BOD = 'BOD'
        BWC = 'BWC'
        DTM = 'DTM'
        GGA = 'GGA'
        GLL = 'GLL'
        GRS = 'GRS'
        GSA = 'GSA'
        GST = 'GST'
        GSV = 'GSV'
        MSK = 'MSK'
        MSS = 'MSS'
        RMA = 'RMA'
        RMB = 'RMB'
        RMC = 'RMC'
        RTE = 'RTE'
        TRF = 'TRF'
        STN = 'STN'
        VBW = 'VBW'
        VTG = 'VTG'
        WCV = 'WCV'
        WPL = 'WPL'
        XTC = 'XTC'
        XTE = 'XTE'
        ZTG = 'ZTG'
        ZDA = 'ZDA'

    @staticmethod
    def is_och_format(message):
        message = message.replace(',', OchUtils.Delimiter)
        return message.count(OchUtils.Delimiter) == len(OchUtils.HEADER_OCH) - 1
