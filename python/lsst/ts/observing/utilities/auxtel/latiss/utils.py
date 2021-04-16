__all__ = ["parse_obs_id"]
from lsst.ts.observatory.control.constants import atcs_constants


def parse_obs_id(obs_id):
    """Split an obsId into its constituent parts ()

    Parameters
    ----------
    obs_id: `str`
        Visit id (e.g. 'AT_O_20200219_000212')

    Returns
    -------
    source: `str`
        Telescope (AT or MT)
    controller: `str`
        O for OCS, C for CCS
    dayObs: `str`
        Date string (e.g. 2021-12-23)
    seqNum: `int`
        Sequence number, which is the last set of values in the obs_id.

    """
    source, controller, dayObs, seqNum = obs_id.split("_")
    dayObs = f"{dayObs[0:4]}-{dayObs[4:6]}-{dayObs[6:8]}"
    seqNum = int(seqNum)

    return source, controller, dayObs, seqNum


def parse_visit_id(visit_id):
    """Return a data_id dictionary from a visit ID.

    Parameters
    ----------
    visit_id: `int` or `str`
        Visit id (e.g. '2021032300308')

    Returns
    -------
    data_id: `dict`
        dictionary with dayObs and seqNum keys
    """
    _visit_id = str(visit_id)
    day_obs = f"{_visit_id[0:4]}-{_visit_id[4:6]}-{_visit_id[6:8]}"
    seq_num = int(_visit_id[9::])

    data_id = dict(dayObs=day_obs, seqNum=seq_num)

    return data_id


def calculate_xy_offsets(target_position, current_position):
    """Returns x/y offset in arcseconds based on current
    and desired position"""

    dx_arcsec, dy_arcsec = atcs_constants.plate_scale * (
        target_position - current_position
    )  # arcsec

    return dx_arcsec, dy_arcsec
