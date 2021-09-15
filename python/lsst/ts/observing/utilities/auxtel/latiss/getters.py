import time
import asyncio
import lsst.daf.butler as dafButler
import logging
from lsst.rapid.analysis import BestEffortIsr

STD_TIMEOUT = 10  # seconds

logging.basicConfig()
# Make matplotlib less chatty
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def get_image(
    data_id,
    dataset="quickLookExp",
    datapath="/repo/main/",
    timeout=STD_TIMEOUT,
    runBestEffortIsr=True,
    loop_time=0.1,
):
    """
    Retrieve image from butler repository.
    If not present, then it will poll at intervals of loop_time (0.1s default)
    until the image arrives, or until the timeout is reached.

    Parameters
    ----------
    dataset: `string`
        dataset to use when grabbing image.
        Examples include: 'raw','quickLookExp' (default)
    datapath: `string`
        Directory of butler repository
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
    while time.time() < endtime:
        # try to retrieve the image
        try:
            logger.debug(
                f"Pulling data with dataset = {dataset} and dataId = {data_id}"
            )
            #             butler.dataRef(dataset, dataId=data_id)
            butler = dafButler.Butler(
                datapath, instrument="LATISS", collections="LATISS/raw/all"
            )
            break
        except RuntimeError:
            logger.warning(
                f"Could not get new image from butler. Waiting "
                f"{loop_time} seconds and trying again."
            )
            await asyncio.sleep(loop_time)
    else:
        raise TimeoutError(f"Unable to get raw image from butler in {timeout} seconds.")

    # Found the image, Run bestEffortISR or just return in the image?
    if runBestEffortIsr:
        logger.debug(f"Running bestEffort ISR on {data_id} from datapath={datapath} and returning exposure")
        bestEffort = BestEffortIsr(datapath, repodirIsGen3=True)
        bestEffort.writePostIsrImages = False  # Don't write to butler database
        exp = bestEffort.getExposure(data_id)
    else:
        logger.debug(f"Grabbing {data_id} from {dataset} and returning exposure")
        exp = butler.get(dataset, data_id)

    return exp
