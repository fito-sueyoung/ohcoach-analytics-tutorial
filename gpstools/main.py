from gpstools.gp2ochconverter import GpToOchConverter
from gpstools.och2gpconverter import OchToGpConverter

if __name__ == "__main__":

    # ========== convert gp to och
    gpFilepath = "../data/sample.gp"
    ochFilepath = gpFilepath.replace(".gp", ".och")

    gp_file = open(gpFilepath, "r")
    gp_data = gp_file.read()
    gpToOchConverter = GpToOchConverter()
    och_df = gpToOchConverter.convert(gp_data)
    print(och_df)

    # ========== convert och to gp
    # ochFilepath = "./sample.och"
    # och_file = open(ochFilepath, "r")
    # och_data = och_file.read()
    # gpFilepath = ochFilepath.replace(".och", "(1).gp")
    # ochToGpConverter = OchToGpConverter()
    # gp_df = ochToGpConverter.convert(och_data)
    # print(gp_df)
    # ochToGpConverter.generate_gp_file(gpFilepath)
