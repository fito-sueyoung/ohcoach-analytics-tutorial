import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from ohcoachtools.gpscoordtools import gpspoint_to_fieldlocal
from ohcoachtools.myconstants import *
from ohcoachtools.field import Field

if __name__ == '__main__':
    # Load stadium coordinates
    field_filepath = os.path.join(DATA_DIR, 'field_01.csv')
    field_coord = np.array(pd.read_csv(field_filepath, sep=',', header=None))
    field = Field()
    field.set_gps_corners(field_coord)

    # Read gps data
    gps_filepath = os.path.join(DATA_DIR, 'sample_01.och')
    och_df = pd.read_csv(gps_filepath, sep=',', header=0, names=OCH_HEADER)

    # Convert strings to datetimes
    och_df[LABEL_DATETIME] = och_df[LABEL_DATETIME].apply(
        lambda x: datetime.strptime(x, '%Y.%m.%d.%H.%M.%S.%f')
    )
    # Compute local coordinates
    och_df[[LABEL_X, LABEL_Y]] = och_df.apply(
        lambda x: gpspoint_to_fieldlocal(x[LABEL_LATITUDE], x[LABEL_LONGITUDE], field),
        axis=1, result_type='expand'
    )

    # Visualization
    plt.plot(och_df[LABEL_X], och_df[LABEL_Y])
    plt.title('Player Trajectory')
    plt.xlim(0, field.width)
    plt.ylim(0, field.height)
    plt.grid(True)
    plt.show()



