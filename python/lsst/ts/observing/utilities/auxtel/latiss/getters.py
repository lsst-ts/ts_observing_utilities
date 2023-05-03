import asyncio
import logging
import time
import typing

from lsst.afw.image import ExposureF


async def get_image(
    data_id: dict[str, int | str],
    best_effort_isr: typing.Any,
    timeout: float,
    loop_time: float = 0.1,
    log: None | logging.Logger = None,
) -> ExposureF:
    """
    Retrieve image from butler repository.
    If not present, then it will poll at intervals of loop_time (0.1s default)
    until the image arrives, or until the timeout is reached.

    Parameters
    ----------
    data_id : `dict`
        A dictionary consisting of the keys and data required to fetch an
        image from the butler.
        e.g data_id = {'day_obs': 20200219, 'seq_num': 2,
                       'detector': 0, "instrument": 'LATISS'}
    best_effort_isr : `object`
        BestEffortISR class instantiated with a butler.
    loop_time : `float`
        Time between polling attempts. Defaults to 0.1s.
    timeout : `float`
        Total time to poll for image before raising an exception.
    log : `logging.Logger`, optional
        An optional logger to use when logging information. If not given,
        creates one.

    Returns
    -------
    exp: `ExposureF`
        Exposure returned from butler query
    """

    logger = log.getChild("get_image") if log is not None else logging.getLogger("get_image")

    endtime = time.time() + timeout
    while True:
        # try to retrieve the image
        try:
            logger.debug(f"Pulling exposure with dataId = {data_id}")
            exp = best_effort_isr.getExposure(data_id, detector=0)
            logger.debug("Image grabbed and ISR performed successfully")
            return exp

        except ValueError:
            logger.exception(
                f"Could not get new image from butler. Waiting {loop_time} seconds and trying again."
            )
            await asyncio.sleep(loop_time)

        if time.time() >= endtime:
            raise TimeoutError(f"Unable to get raw image from butler in {timeout} seconds.")
