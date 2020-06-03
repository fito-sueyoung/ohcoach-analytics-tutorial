import numpy as np


def llh_to_ecef(latitude, longitude, height):
    a = 6378137.0           # earth semimajor axis
    b = 6356752.3142        # earth semiminor axis
    w = 0.000072921151467   # earth rotation rate in radians
    mu = 398600500000000.   # earth gravitational constant

    f = (a - b) / a             # ellipsoid flatness
    e = np.sqrt(f * (2 - f))    # eccentricity
    latitude = np.radians(latitude)
    longitude = np.radians(longitude)

    # plumb line length stratched to z axis
    N = a / np.sqrt(1 - e * e * np.sin(latitude) * np.sin(latitude))

    ecef = np.zeros(3)
    ecef[0] = (height + N) * np.cos(latitude) * np.cos(longitude)
    ecef[1] = (height + N) * np.cos(latitude) * np.sin(longitude)
    ecef[2] = (height + (1 - e * e) * N) * np.sin(latitude)

    return ecef


def gpspoint_to_fieldlocal(latitude, longitude, field, refoption='bottomleft'):
    if np.isnan(latitude) or np.isnan(longitude):
        return [np.nan, np.nan]
    else:
        # ecef_corner: 4x3 ecef vector of corner points of a soccer field
        ecef_corner = field.ecef_corners

        # Aligned vector with long axis of soccer field
        normedXAxisVector = np.zeros(3)
        normedYAxisVector = np.zeros(3)
        center2TargetVector = np.zeros(3)

        ecef_center = np.zeros(3)  # Center ecef vector
        ecef_center[0] = (ecef_corner[0][0] + ecef_corner[1][0] + ecef_corner[2][0] + ecef_corner[3][0]) / 4
        ecef_center[1] = (ecef_corner[0][1] + ecef_corner[1][1] + ecef_corner[2][1] + ecef_corner[3][1]) / 4
        ecef_center[2] = (ecef_corner[0][2] + ecef_corner[1][2] + ecef_corner[2][2] + ecef_corner[3][2]) / 4
        ecef_target = llh_to_ecef(latitude, longitude, 0)

        # Get vector from ECEF vectors
        for i in range(3):
            normedXAxisVector[i] = ecef_corner[0][i] - ecef_corner[1][i]
            normedYAxisVector[i] = ecef_corner[1][i] - ecef_corner[2][i]
            center2TargetVector[i] = ecef_target[i] - ecef_center[i]

        # Normalizing X basis vectorno
        tmpScalar = np.sqrt(
            np.power(normedXAxisVector[0], 2) + np.power(normedXAxisVector[1], 2) + np.power(normedXAxisVector[2], 2))
        for i in range(3):
            normedXAxisVector[i] /= tmpScalar
        # Normalizing Y basis vector
        tmpScalar = np.sqrt(
            np.power(normedYAxisVector[0], 2) + np.power(normedYAxisVector[1], 2) + np.power(normedYAxisVector[2], 2))
        for i in range(3):
            normedYAxisVector[i] /= tmpScalar

        # Projecting center2target vector to each vector
        tmpCoord = [0, 0]  # coordinate of the present GPS point w.r.t center (a.k.a. origin) in meter scale

        for i in range(3):
            tmpCoord[0] += center2TargetVector[i] * normedXAxisVector[i]
            tmpCoord[1] += center2TargetVector[i] * normedYAxisVector[i]

        # point = pd.Series(index=[LABEL_X, LABEL_Y])
        # Reference point: field center
        point = [tmpCoord[0] * 100, tmpCoord[1] * 100]

        if not (refoption == 'center' or refoption == 'bottomleft' or refoption == 'topleft'):
            refoption = 'bottomleft'

        if refoption == 'bottomleft':
            point[0] = point[0] + field.width / 2.0
            point[1] = point[1] + field.height / 2.0
        elif refoption == 'topleft':
            point[0] = point[0] + field.width / 2.0
            point[1] = -point[1] + field.height / 2.0
        return [int(i) for i in point]
