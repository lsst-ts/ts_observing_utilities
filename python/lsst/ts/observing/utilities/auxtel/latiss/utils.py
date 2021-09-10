__all__ = ["parse_obs_id"]

from lsst.ts.observatory.control.constants import latiss_constants

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
    source, controller, day_obs, seq_num = obs_id.split("_")
    day_obs = int(f"{day_obs[0:4]}{day_obs[4:6]}{day_obs[6:8]}")
    seq_num = int(seq_num)

    return source, controller, day_obs, seq_num


def parse_visit_id(visit_id):
    """Return a data_id dictionary from a visit ID.
    The dictionary is formatted for a gen3 butler.

    Parameters
    ----------
    visit_id: `int` or `str`
        Visit id (e.g. '2021032300308')

    Returns
    -------
    data_id: `dict`
        dictionary with newly derived day_obs and seq_num keys
    """
    _visit_id = str(visit_id)
    day_obs = int(f"{_visit_id[0:4]}{_visit_id[4:6]}{_visit_id[6:8]}")
    seq_num = int(_visit_id[9::])

    data_id = {'day_obs': day_obs, 'seq_num': seq_num, 'detector': 0, "instrument": 'LATISS'}

    return data_id


def calculate_xy_offsets(target_position, current_position):
    """Returns x/y offset in arcseconds based on current
    and desired position"""

    dx_arcsec, dy_arcsec = latiss_constants.pixel_scale * (
        target_position - current_position
    )

    return dx_arcsec, dy_arcsec
