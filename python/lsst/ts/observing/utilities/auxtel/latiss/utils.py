__all__ = ["parse_obs_id"]
from lsst.ts.observatory.control.constants import atcs_constants


def parse_obs_id(obs_id):
    """Split an obsId into its constituent parts

    E.g.
        parse_obs_id('AT_O_20200219_000212')
    """
    source, controller, dayObs, seqNum = obs_id.split("_")
    dayObs = f"{dayObs[0:4]}-{dayObs[4:6]}-{dayObs[6:8]}"
    seqNum = int(seqNum)

    return source, controller, dayObs, seqNum


def calculate_xy_offsets(target_position, current_position):
    """Returns x/y offset in arcseconds based on current
    and desired position"""

    dx_arcsec, dy_arcsec = atcs_constants.plate_scale * (
        target_position - current_position
    )  # arcsec

    return dx_arcsec, dy_arcsec
