import numpy as np
from . import gpscoordtools as gps


class Field:
    def __init__(self):
        self.name = ""
        self.gps_corners = np.zeros((4, 2))
        self.ecef_corners = np.zeros((4, 3))
        self.width = 0
        self.height = 0
        
    def set_name(self, name):
        self.name = name
    
    def set_gps_corners(self, points):
        self.gps_corners = points.reshape(4, 2)
        self.compute_ecef_corners()
        
    def compute_ecef_corners(self):
        gps_corners = self.gps_corners
        ecef_corners = np.zeros([4, 3])
        
        for i in range(4):
            ecef_corners[i, :] = gps.llh_to_ecef(gps_corners[i, 0], gps_corners[i, 1], 0)

        # get field width/height
        length01 = np.sqrt(np.power(ecef_corners[0, 0] - ecef_corners[1, 0], 2) +
                           np.power(ecef_corners[0, 1] - ecef_corners[1, 1], 2) +
                           np.power(ecef_corners[0, 2] - ecef_corners[1, 2], 2))
        length10 = np.sqrt(np.power(ecef_corners[2, 0] - ecef_corners[1, 0], 2) +
                           np.power(ecef_corners[2, 1] - ecef_corners[1, 1], 2) +
                           np.power(ecef_corners[2, 2] - ecef_corners[1, 2], 2))
        width = np.maximum(length01, length10) * 100
        height = np.minimum(length01, length10) * 100

        # rotate corner indices
        if length01 < length10:
            p0 = gps_corners[1, :]
            p1 = gps_corners[2, :]
            p2 = gps_corners[3, :]
            p3 = gps_corners[0, :]
            gps_corners[0, :] = p0
            gps_corners[1, :] = p1
            gps_corners[2, :] = p2
            gps_corners[3, :] = p3
            
            p0 = ecef_corners[1, :]
            p1 = ecef_corners[2, :]
            p2 = ecef_corners[3, :]
            p3 = ecef_corners[0, :]
            ecef_corners[0, :] = p0
            ecef_corners[1, :] = p1
            ecef_corners[2, :] = p2
            ecef_corners[3, :] = p3

        self.gps_corners = gps_corners
        self.ecef_corners = ecef_corners
        self.width = width.round(0)
        self.height = height.round(0)

