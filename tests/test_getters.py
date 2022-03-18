# This file is part of ts_observing_utilities
#
# Developed for the LSST Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

import asynctest
import logging
import pathlib

logging.basicConfig()
# Make matplotlib less chatty
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.propagate = True

# See if data is available from current location
# Expect to run from Tucson test stand but no data exists
# there at this time.

DATAPATH = pathlib.Path("/repo/LATISS")  # for the summit
try:
    from lsst.ts.observing.utilities.auxtel.latiss.getters import get_image

    import lsst.daf.butler as dafButler
    from lsst.rapid.analysis import BestEffortIsr
    import lsst.afw.image as afwImage

    BUTLER = dafButler.Butler(
        DATAPATH.as_posix(), instrument="LATISS", collections="LATISS/raw/all"
    )
    DATA_AVAILABLE = True
except ModuleNotFoundError:
    logger.warning("Data unavailable, certain tests will be skipped")
    DATA_AVAILABLE = False


@asynctest.skipIf(DATA_AVAILABLE is False, "No data available")
class TestGetters(asynctest.TestCase):
    async def test_get_image(self):
        day_obs = 20211104
        seq_num = 950
        data_id = {
            "day_obs": day_obs,
            "seq_num": seq_num,
            "detector": 0,
            "instrument": "LATISS",
        }

        best_effort_isr = BestEffortIsr(DATAPATH.as_posix())

        # BestEffortISR will run be default
        logger.debug("Starting test with ISR enabled")
        exp = await get_image(
            data_id,
            best_effort_isr,
            timeout=10,
        )

        # Not sure how to assert if things ran properly but if it errors
        # then an exception is raised and the test will fail
        self.assertTrue(isinstance(exp, afwImage.Exposure))

        logger.debug("Running test of get_image when image is not in butler")
        day_obs = 18540315  # This is an invalid ID and does not have an image
        data_id = {
            "day_obs": day_obs,
            "seq_num": seq_num,
            "detector": 0,
            "instrument": "LATISS",
        }
        with self.assertRaises(TimeoutError):
            await get_image(
                data_id,
                best_effort_isr,
                timeout=3,
            )
