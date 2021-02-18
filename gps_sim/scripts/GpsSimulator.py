import numpy as np
from GpsNoiser import GpsNoiser
from Magnetometer import Magnetometer

class GpsSimulator:

    def __init__(self):
        self._rtk_noiser = GpsNoiser()
        self._float_noiser = GpsNoiser()
        self._ppk_noiser = GpsNoiser()

        self._ppk_output_cov = np.eye(3)
        self._float_output_cov = np.eye(3)
        self._rtk_output_cov = np.eye(3)

        self._mag_noiser = Magnetometer()

        # can be: auto, none, ppk, float, rtk
        self._current_mode = "auto"

        self._rtk_polygon = []
        self._ppk_polygon = []
        self._float_polygon = []
        self._none_polygon = []

    def set_mode(self, mode):
        self._current_mode = mode

    def get_mag(self, input_pose):
        input_orientation = np.eye(3)
        return self._mag_noiser.getMagneticField(input_orientation)

    def get_gps(self, input_pose, fixtype):
        if fixtype is "none":
            # *screaming" lost fix!!
            return None, None

        input_enu = np.zeros([0, 0, 0])
        output_enu = np.zeros([0, 0, 0])
        output_cov = np.eye(3)

        if fixtype is "rtk":
            output_enu = self._rtk_noiser.perturb(input_enu)
            output_cov = self._rtk_output_cov

        elif fixtype is "float":
            output_enu = self._float_noiser.perturb(input_enu)
            output_cov = self._float_output_cov

        elif fixtype is "ppk":
            output_enu = self._ppk_noiser.perturb(input_enu)
            output_enu = self._ppk_output_cov

        return output_enu, output_cov

    def get_fixtype(self, input_pose):
        return "auto" # for now

    def simulate(self, input_pose):
        # output GPS
        if self._current_mode is "auto":
            fixtype = self.get_fixtype(input_pose)
            output_enu, output_cov = self.get_gps(input_pose, fixtype)
        else:
            output_enu, output_cov = self.get_gps(input_pose, self._current_mode)

        output_mag = self.get_mag(input_pose)

        # weird pythonic flex that these variables are found
        return output_enu, output_cov, output_mag
