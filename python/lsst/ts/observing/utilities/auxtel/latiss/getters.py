import time
import lsst.daf.persistence as dafPersist
import logging
from lsst.rapid.analysis import BestEffortIsr
from lsst.ts.observing.utilities.auxtel.latiss.utils import parse_obs_id

STD_TIMEOUT = 10  # seconds

logging.basicConfig()
# Make matplotlib less chatty
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def get_next_image_dataId(latiss, timeout=STD_TIMEOUT, flush=True):
    """Return dataID of image that appears from the ATArchiver CSC.
    This is meant to be called at the same time as a take image command.
    If this is called after take_image is completed, it may not receive
    the imageInOODS event.

    Inputs:
    Must supply the latiss class as first argument
    """

    logger.info(
        f"Waiting for image to arrive in OODS for a maximum of {timeout} seconds."
    )
    in_oods = await latiss.rem.atarchiver.evt_imageInOODS.next(
        timeout=timeout, flush=flush
    )

    dayObs, seqNum = parse_obs_id(in_oods.obsid)[-2:]
    logger.info(f"seqNum {seqNum} arrived in OODS")

    dataId = dict(dayObs=dayObs, seqNum=seqNum)

    return dataId


async def get_image(
    dataId,
    dataset="quickLookExp",
    datapath="/project/shared/auxTel/",
    timeout=STD_TIMEOUT,
    runBestEffortIsr=True,
):
    """Retrieve image from butler repository.
    If not present, then it will poll at 0.1s intervals until the image
    arrives, or until the timeout is reached.

    Inputs:
    dataset: dataset to use when grabbing image.
        Examples include: 'raw','quickLookExp' (default)
    datapath: directory of butler repository
    """

    endtime = time.time() + timeout
    _loop_time = 0.1  # [s]
    while time.time() < endtime:
        # refresh butler repo
        butler = dafPersist.Butler(datapath)
        # try to retrieve the image
        try:
            logger.debug(f"Pulling data with dataset = {dataset} and dataId = {dataId}")
            butler.dataRef(dataset, dataId=dataId)
            break
        except RuntimeError:
            logger.warning(
                f"Could not get new image from butler. Waiting "
                f"{_loop_time}s and trying again."
            )
            time.sleep(_loop_time)
    else:
        raise TimeoutError(f"Unable to get raw image from butler in {timeout} seconds.")

    # Found the image, Run bestEffortISR or just return in the image?
    if runBestEffortIsr:
        logger.debug(f"Running bestEffort ISR on {dataId} and returning image")
        bestEffort = BestEffortIsr(datapath)
        bestEffort.writePostIsrImages = False  # Don't write to butler database
        exp = bestEffort.getExposure(dataId)
    else:
        logger.debug(f"Grabbing {dataId} from {dataset} and returning image")
        exp = butler.get(dataset, dataId)

    return exp
