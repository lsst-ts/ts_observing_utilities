import time
import asyncio
import logging

STD_TIMEOUT = 10  # seconds

logging.basicConfig()
# Make matplotlib less chatty
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def get_image(
    data_id,
    best_effort_isr,
    timeout=STD_TIMEOUT,
    loop_time=0.1,
):
    """
    Retrieve image from butler repository.
    If not present, then it will poll at intervals of loop_time (0.1s default)
    until the image arrives, or until the timeout is reached.

    Parameters
    ----------
    data_id: `dict`
        A dictionary consisting of the keys and data required to fetch an
        image from the butler.
        e.g data_id = {'day_obs': 20200219, 'seq_num': 2,
                       'detector': 0, "instrument": 'LATISS'}
    best_effort_isr: `object`
        BestEffortISR class instantiated with a butler.
    loop_time: `float`
        Time between polling attempts. Defaults to 0.1s
    timeout: `float`
        Total time to poll for image before raising an exception

    Returns
    -------

    exp: `ExposureF`
        Exposure returned from butler query
    """
    endtime = time.time() + timeout
    while True:
        # try to retrieve the image
        try:
            logger.debug(f"Pulling exposure with dataId = {data_id}")
            exp = best_effort_isr.getExposure(data_id)
            logger.debug("Image grabbed and ISR performed successfully")
            return exp

        except RuntimeError:
            logger.warning(
                f"Could not get new image from butler. Waiting "
                f"{loop_time} seconds and trying again."
            )
            await asyncio.sleep(loop_time)

        if time.time() >= endtime:
            raise TimeoutError(
                f"Unable to get raw image from butler in {timeout} seconds."
            )
